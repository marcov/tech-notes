# Processes

## procfs Interface

TIL: `/proc/PID`: the owner user group IDs shown when calling `stat` on this
directory corresponds to the credentials ot `PID`.

## Process IDs

(Get IDs from: `/proc/PID/status`)

- PID: the process ID.
- PPID: the parent Process ID that created the process (PPID of PID1 is 0).
- PGID: the process' Group ID.

  * Process Group = a collection of related processes.
  * Process Group Leader = the first member of a process group (its PID is the
    PGID).
  * A PID may join another Process Group
  * The process group leader need not be the last member of a process group.
  * The shell starts each executable in a new process group. When the executable
    runs, its PID == PGID.
  * When running a pipeline of executables,the shell create a new process group
    and places all executables in the pipeline in that group. The leader is the
    first member of the pipeline.

- SID: the process' Session ID.

  * Session = collection of related Process Groups.
  * Session Leader = the process that created the session (its own PID becomes
    the SID).
  * All processes in a session share the same controlling terminal, established
    when the leader opens a terminal device.
  * Each terminal window has a separate Session.

*Process Groups* and *Sessions* are abstraction to support shell job control,
e.g. allow interactive users to run command in fg / bg.


## Symbolic process stack

`/proc/[pid]/stack`: This file provides a symbolic trace of the function calls in
this process's kernel stack.

## Zombie vs Orphan

- Orphan: a process whose parent has terminated, but that it is still in
  execution.

- Zombie: a process that has completed execution (i.e., called `exit()`), but
  has still an entry in the process table. The entry stays there until the
  parent retrieves the child exit status using `waitpid()`.

In both cases, when the parent dies / terminates without calling `wait()`, the
orphan or zombie child is "adopted" by init (it is `wait()`'ed by init) and it
is hence reaped.

*Reaping* = the action of calling `waitpid()` on a process.

When a child terminates, the OS sends a SIGCHLD signal to the parent process,
so that is has a chance to reap the child.

>
> More info: https://blog.phusion.nl/2015/01/20/docker-and-the-pid-1-zombie-reaping-problem/
>

For containers using PID namespaces the kernel, when forgetting the original
parent and finding the child reaper, may call `zap_pid_ns_processes()`. This
has the effect of killing all the pids in that PID NS using
`group_send_sig_info(SIGKILL, SEND_SIG_PRIV, pid)` This happens when the reaper
is the parent that is exiting, and the parent has not other threads active that
could reap.

## Child subrepaer

A process can specify itself as the "child subreaper" for all its
descendants, ie. the process that will reap all descendants.
It does so by calling:

```c
prctl(PR_SET_CHILD_SUBREAPER, 1);
```

A subreaper fulfills the role of init for its descendant processes.
When a descendant becomes orphaned, it will be reaped by this process instead
of by init.

The setting persist after calling exec(), ie. the executed process will be
the subreaper.

The setting is cleared after calling fork(), ie. the forked child will not be
a subreaper.

## Create a session leader

Use the `setsid()` syscall.
This will clear out the process controlling tty.

- A new pty master/slave pair is allocated with `posix_openpt()`.
- The session leader acquires a controlling terminal with `ioctl(fd, TIOCSCTTY, ...)`
  `fd` is typically the slave fd of a pty master/slave pair.

## Making a child exit

When you need a child to exit, it should call `_exit(retno)` and not
`exit(retno)`.

`exit(retno)` causes all `atexit(...)` registered handlers to fire, and e.g.
all temporary files created with `tmpfile()` to be deleted.

Besides, the raw `_exit()` terminates only the calling thread.

## File Descriptors

### Sharing fds between processes

- Use `SCM_RIGHTS`: pass a fd b/w processes using UNIX sockets.

## User Mode and Kernel mode stacks

When running in kernel mode, the process uses a kernel-private stack.
