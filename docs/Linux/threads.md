# Linux Threads

## Thread IDs

 - TID: the Thread ID

   * In a single threaded process, TID = PID = TGID
   * In a multi threaded process, all threads have the same PID, but each one has
     a unique TID.
   * TIDs are unique system-wide.
   * Threads / TIDs created with the CLONE_THREAD flag.
   * What's my TID? Use `gettid()`

 - TGID: the Thread Group ID.

   * Thread Group = a group of KSEs (Kernel Scheduling Entities) that share the
     same TGID.
   * Each thread in a thread group has a distint TID.
   * Thread Group Leader = the first thread in a new thread group, where TID ==
     TGID
   * TGID == PID
   * A TGID can exit independently from the other TIDs by calling `pthread_exit()`.
     In that case, the TGID becomes a zombie but it is not reapable until
     all the other threads in the group exit.

 - All the TIDs for a TGID show up under `/proc/TGID/task/{TID1,TID2, ...}`
   Contrary to PIDs, the  `/proc/[tid]` subdirectories are not visible when
   iterating through `/proc` with `getdents(2)` (and thus are not visible when
   one uses ls(1) to view the contents of /proc).

## Threads and clone()

When you create a thread using `clone(flags = CLONE_THREAD)`, keep in mind
that:

- the created thread will share the parent process with the caller of clone,
- hence the caller of clone **cannot** call `wait()` to wait for the
  termination / reap the created thread.

>
> A new thread created with CLONE_THREAD has the same parent process as the
> caller of clone() (i.e., like CLONE_PARENT),  so that  calls to getppid(2)
> return the same value for all of the threads in a thread group.  When a
> CLONE_THREAD thread ter‐ minates, the thread that created it using clone() is
> not sent a SIGCHLD (or other termination) signal; nor can the  status of such
> a thread be obtained using wait(2).  (The thread is said to be detached.)
>

## Threads and exec()

When a thread (TID) calls the exec() syscall, all other threads other than the
calling thread are destroyed. The calling thread gets as PID (TID) the TGID.

## _Satefy_

- Thread safe function: function that can be _safely_ called (concurrently) by
  multiple thread. Typically, immune to data races.

- _async-signal-safe_ function: function that can be _safely_ called
  (concurrently) by a signal handler.

- Re-entrant functions: a function that can be invoked multiple times
  concurrently. I.e., it can be interrupted, and called again before the
  interruption to complete.

### Consequences
```
 non-reentrant => non-thread-safe

 non-reentrant => non-async-signal-safe

 statically allocated data in a function => non-reentrant function.
```

## pthreads and TCB

The thread control block (TCB) for pthread stores a (struct pthread) structure.
Its address is stored in the FS register:

More details:
- https://fasterthanli.me/series/making-our-own-executable-packer/part-13
- `struct pthread` definition inside glibc `nptl/descr.h`.
- glibc `nptl/allocatestack.c`

TCB and TLS areas sits at the end of the thread stack:
- For x86, TLS is before the struct.
- For arm64, TLS is after (struct pthread).

```
Thread stack:
                address stored in CPU FS register ($fs_base)
                                 ^
                                 |
 [ stack start            |               stack top ]
 ^                      | TLS  | TCB <-------------.
 |                             | struct pthread    |
 |                             | {                 |
 |                                    tcbhead_t    |
 |                                    {            |
 |                                        tcb ->---`
 |                                    }
 |
 |                                   stackblock ->-.
 |                                                 |
 |                               }                 v
 `-------------------------------------------------`
```

The `pthread_t thread_id` is in fact the address of the TCB.

DTV: Dynamic thread vector, which is a mapping from module ID to
thread-local storage (?)

### glibc details

`struct pthread` contains thread specific attributes and information.
(`struct pthread`) == (`pthread_t` made as a pointer)

- `stackblock` -> base returned from mmap in `allocate_stack()`
- `stackblock_size` -> size passed to mmap in `allocate_stack()`. Includes `guardsize`.

## Threads and credentials

### `setuid()` - glibc
From the glibc manual:
    NPTL and process credential changes
    At the Linux kernel level, credentials (user and group IDs) are a
    per-thread attribute. However, POSIX requires that all of the
    POSIX threads in a process have the same credentials. To
    accommodate this requirement, the NPTL implementation wraps all
    of the system calls that change process credentials with
    functions that, in addition to invoking the underlying system
    call, arrange for all other threads in the process to also change
    their credentials.

    The implementation of each of these system calls involves the use
    of a real-time signal that is sent (using tgkill(2)) to each of
    the other threads that must change its credentials. Before
    sending these signals, the thread that is changing credentials
    saves the new credential(s) and records the system call being
    employed in a global buffer. A signal handler in the receiving
    thread(s) fetches this information and then uses the same system
    call to change its credentials.

    Wrapper functions employing this technique are provided for
    setgid(2), setuid(2), setegid(2), seteuid(2), setregid(2),
    setreuid(2), setresgid(2), setresuid(2), and setgroups(2).

    NPTL real-time signals
    NPTL makes internal use of the first two real-time signals
    (signal numbers 32 and 33). One of these signals is used to
    support thread cancellation and POSIX timers (see
    timer_create(2)); the other is used as part of a mechanism that
    ensures all threads in a process always have the same UIDs and
    GIDs, as required by POSIX. These signals cannot be used in
    applications.

    - The sigprocmask(2) and pthread_sigmask(3) interfaces silently
    ignore attempts to block these two signals.
    - sigfillset(3) does not include these two signals when it
    creates a full signal set.
