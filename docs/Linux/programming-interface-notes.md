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

### Zombie vs orphan
- Orphan: a process whose parent has terminated, but that is still in execution.

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

## Threads
### Thread IDs
 - TID: the Thread ID
   * In a single threaded process, TID = PID
   * In a multi threaded process, all threads have the same PID, but each one has
     a unique TID.
   * TIDs are unique system-wide.
 - TGID: the Thread Group ID.
   * Thread Group = a group of KSEs (Kernel Scheduling Entities) that share the same TGID.
   * Each thread in a thread group has a distint TID.
   * Thread Group Leader = the first thread in a new thread group, where TID == TGID
   * TGID == PID

>
> **NOTE**: you cannot "kill" a single thread ID without killing all the TIDs in the
> TGID (i.e. the PID). From `pthread_kill(3)` (implemented using `tgkill()`):
>
> Signal  dispositions  are process-wide: if a signal handler is installed, the handler will
> be invoked in the thread  thread,  but  if  the  disposition  of  the  signal  is  "stop",
> "continue", or "terminate", this action will affect the whole process.
>

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
