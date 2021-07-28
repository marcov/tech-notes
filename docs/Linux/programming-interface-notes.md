# Notes on the Linux Programming Interface

## How To Call a Syscall

-  Use `syscall()`:
```
syscall(SYS_kill, pid, signum);
```

- Use inline asm:
```
//
// 57 is the syscall number for fork()
// the return value is stored in the pid variable
//
int pid;
asm("mov    $57, %%eax\n syscall\n" : "=r" (pid));
```
## Processes
### Process IDs
(Get IDs from: `/proc/PID/status`)

- PID: the process ID.
- PPID: the parent Process ID that created the process (PPID of PID1 is 0).
- PGID: the process' Group ID.
  * Process Group = a collection of related processes.
  * Process Group Leader = the process that created the group (its own PID becomes
    the PGID).
  * A PID may join another Process Group
- SID: the process' Session ID.
  * Session = collection of related Process Groups.
  * Session Leader = the process that created the session (its own PID becomes
    the SID).
  * All processes in a session share the same controlling terminal, established
    when the leader opens a terminal device.
  * Each terminal window has a separate Session.

*Process Groups* and *Sessions* are abstraction to support shell job control,
e.g. allow interactive users to run command in fg / bg.

### Symbolic process stack
`/proc/[pid]/stack`: This file provides a symbolic trace of the function calls in
this process's kernel stack.

### Zombie vs Orphan
- Orphan: a process whose parent has terminated, but that it is still in execution.

- Zombie: a process that has completed execution (i.e., called `exit()`), but has
  still an entry in the process table. The entry stays there until the parent
  retrieves the child exit status using `waitpid()`.

In both cases, when the parent dies / terminates without calling `wait()`, the
orphan or zombie child is "adopted" by init (it is `wait()`'ed by init) and it is
hence reaped.

*Reaping* = the action of calling `waitpid()` on a process.

When a child terminates, the OS sends a SIGCHLD signal to the parent process,
so that is has a chance to reap the child.

>
> More info: https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem/
>

For containers using PID namespaces the kernel, when forgetting the original parent
and finding the child reaper, may call `zap_pid_ns_processes()`.
This has the effect of killing all the pids in that PID NS using `group_send_sig_info(SIGKILL, SEND_SIG_PRIV, pid)`
This happens when the reaper is the parent that is exiting, and the parent
has not other threads active that could reap.

### Create a session leader
Use the `setsid()` syscall.
This will clear out the process controlling tty.
- A new pty master/slave pair is allocated with `posix_openpt()`.
- The session leader acquires a controlling terminal with `ioctl(fd, TIOCSCTTY, ...)`
  `fd` is typically the slave fd of a pty master/slave pair.

## Signals

Signal disposition: what the process does when it receives a specific signal. It can
be one of:
- TERM
- IGN
- CORE
- STOP
- CONT

A process can change that action using `sigaction()` or `signal()`. The change can be:
- perform the default action
- Ignore
- Catch the signal with a signal handler function

You cannot however change the dispostion for `SIGKILL` and `SIGSTOP`.

The signal disposition is a **per-process** attribute. So the action will be the same
**for all the threads**.

## Threads

### Thread IDs

 - TID: the Thread ID
   * In a single threaded process, TID = PID = TGID
   * In a multi threaded process, all threads have the same PID, but each one has
     a unique TID.
   * TIDs are unique system-wide.
   * Threads / TIDs created with the CLONE_THREAD flag.
   * What's my TID? Use `gettid()`

 - TGID: the Thread Group ID.
   * Thread Group = a group of KSEs (Kernel Scheduling Entities) that share the same TGID.
   * Each thread in a thread group has a distint TID.
   * Thread Group Leader = the first thread in a new thread group, where TID == TGID
   * TGID == PID

 - All the TIDs for a TGID show up under `/proc/TGID/task/{TID1,TID2, ...}`
   Contrary to PIDs, the  `/proc/[tid]` subdirectories are not visible when iterating through `/proc`
   with `getdents(2)` (and thus are not visible when one uses ls(1) to view the contents of /proc).

### Threads and signals

A signal may be process-directed or thread-directed.
When process-directed, the signal is delivered to one of the thread that does
not have the signal blocked.

Each thread in a process has an independent signal mask, which indicates the set
of signals that the thread is currently blocking. Use `sigprocmask()` to change the
mask.

**NOTE**: you cannot "SIGKILL" a single thread ID without killing all the TIDs in the
TGID (i.e. the PID). Quoting `pthread_kill(3)` (implemented using `tgkill()`):
>
> Signal  dispositions  are process-wide: if a signal handler is installed, the handler will
> be invoked in the thread,  but  if  the  disposition  of  the  signal  is  "stop",
> "continue", or "terminate", this action will affect the whole process.
>

### Threads and clone()

When you create a thread using clone(flags = CLONE_THREAD), keep in mind that:
- the created thread will share the parent process with the caller of clone,
- hence the caller of clone **cannot** call wait() to wait for the termination / reap
  the created thread.

>
> A new thread created with CLONE_THREAD has the same parent process as the caller of clone() (i.e., like CLONE_PARENT),  so
> that  calls to getppid(2) return the same value for all of the threads in a thread group.  When a CLONE_THREAD thread ter‐
> minates, the thread that created it using clone() is not sent a SIGCHLD (or other termination) signal; nor can the  status
> of such a thread be obtained using wait(2).  (The thread is said to be detached.)
>

### Threads and exec()

When a thread (TID) calls the exec() syscall, all other threads other than the calling
thread are destroyed. The calling thread gets as PID (TID) the TGID.

## _Satefy_
- Thread safe function: function that can be _safely_ called (concurrently) by
  multiple thread. Typically, immune to data races.

- _async-signal-safe_ function: function that can be _safely_ called (concurrently) by
  a signal handler.

- Re-entrant functions: a function that can be invoked multiple times concurrently.
  I.e., it can be interrupted, and called again before the interruption to complete.

### Consequences
```
 non-reentrant => non-thread-safe

 non-reentrant => non-async-signal-safe

 statically allocated data in a function => non-reentrant function.
```

## File Descriptors
### Sharing fds between processes
- Use `SCM_RIGHTS`: pass a fd b/w processes using UNIX sockets.

## File System
```
filename -> inode identifier -> inode reference
                                 / | \
                                /  |  \
                               /   |   \
                        [data0] [data1] [data2] ...
```

### inode
- Unique identifier for a file object.
- File metadata

### dentry
Translates between file name and inode. There is a cache for both dentries and inodes.

## select() vs. poll()
TL;DR: Use `poll()` instead of `select()`
Reasons:
 - select() has poor performances (for-loop from FD 0 to target FD).
 - select() can destroy your stack, if checking for a FD larger than FD_SETSIZE.

More info: https://beesbuzz.biz/code/5739-The-problem-with-select-vs-poll

# `setuid()` - glibc
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

