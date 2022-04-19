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

>
> NOTE: Beware of the difference b/w signal masking & signal handing.
> - A signal can be blocked individually by each thread (sigprocmask())
> - The way a signal is handled it is the same for all the threads in the group (sigaction()).
>

If a signal handler is invoked while a system call or library function call is blocked, then either:
- the call is automatically restarted after the signal handler returns; or
- the call fails with the error EINTR.
Which of these two behaviors occurs depends on the interface and whether or not the signal handler was  estab‐
lished using the SA_RESTART flag (see sigaction(2)).  The details vary across UNIX systems; below, the details

**WARNING**:

Blocking a signal, and changing the signal disposition to ignored is not
the same thing!
If you ignore a signal, the signal will never be received. If you block it instead,
you are still able to wait for it with `sigwait()`.
So typically if you want to use signals to synchronize b/w two processes you could
use:
```c
const int sync_signal = SIGUSR1;

pid_t pid = fork();
if (pid == 0)
{
    //child
    sigset_t set;
    sigemptyset(&set);
    sigaddset(&set, sync_signal);

    sigprocmask(SIG_BLOCK, &set, nullptr);

    int sig = 0;
    sigwait(&set, &sig);
    assert(sync_signal == sig);
}
else
{
    // parent
    kill(pid, sync_signal);
}
```

### Signaling Yourself

Use `raise(3)`. Can be used to do cleanup of specific signals like SIGSTOP and SIGSUSP (C-z).

### Threads and signals

A signal may be process-directed or thread-directed.
When process-directed, the signal is delivered to one of the thread that does
not have the signal blocked.

Each thread in a process has an independent signal mask, which indicates the set
of signals that the thread is currently blocking. Use `sigprocmask()` to change the
mask.

**NOTE**: you cannot "SIGKILL" a single thread ID without killing all the TIDs in the
group (i.e. TGID or PID). Quoting `pthread_kill(3)` (implemented using `tgkill()`):
>
> Signal  dispositions  are process-wide:
> - if a signal handler is installed, that same handler will be invoked for all the
>   threads in the group. Which thread wil run the handler? It's the thread (PID)
>   that got the signal. Different threads cannot have different handlers!
> - If the disposition of the  signal is STOP, CONT, TERMINATE, this action will
>   affect all the threads of the process.
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

