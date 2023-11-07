## Linux Signals

Signal disposition: what the process does when it receives a specific signal.
It can be one of:

- TERM
- IGN
- CORE
- STOP
- CONT

A process can change that action using `sigaction()` or `signal()`. The change
can be:

- Perform the default action
- Ignore
- Catch the signal with a signal handler function

You cannot however change the dispostion for `SIGKILL` and `SIGSTOP`.

In addition, there are a few signals that when sent by the kernel are "forced"
with default dispotion on the process. See kernel's `force_sig_fault()`,
`force_fatal_signal()` et al.

The signal disposition is a **per-process** attribute. So the action will be
the same **for all the threads**.

>
> NOTE: Beware of the difference b/w signal masking & signal handing.
>
> - A signal can be blocked individually by each thread (sigprocmask())
> - The way a signal is handled it is the same for all the threads in the group
>   (sigaction()).
>

If a signal handler is invoked while a system call or library function call is
blocked, then either:

- the call is automatically restarted after the signal handler returns; or
- the call fails with the error EINTR. Which of these two behaviors occurs
  depends on the interface and whether or not the signal handler was  estab‐
  lished using the SA_RESTART flag (see sigaction(2)).  The details vary across
  UNIX systems; below, the details

**WARNING**:

Blocking a signal, and changing the signal disposition to ignored is not the
same thing! If you ignore a signal, the signal will never be received. If you
block it instead, you are still able to wait for it with `sigwait()`. So
typically if you want to use signals to synchronize b/w two processes you could
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

### SIGCHLD

The parent receives this signal when one of its children change of state (could be
suspend, continue or exit). Use wait to figure  out what happened.

### wait() / waitpid() and wait status

- WIFEXITED(): The process exited by calling exit(). Get the return code with
  WEXITSTATUS().

- WIFSIGNALED(): The process exited by the reception of a signal whose
  disposition is to terminate. Get the return code WTERMSIG().

### Signaling Yourself

Use `raise(3)`. Can be used to do cleanup of specific signals like SIGSTOP and
SIGSUSP (C-z).

### Threads and signals

A signal may be **process-directed** (TGID) or **thread-directed** (TID). When
process-directed, the signal is delivered to one of the thread that does not
have the signal blocked.

Each thread in a process has an independent signal mask, which indicates the
set of signals that the thread is currently blocking. Use `sigprocmask()` to
change the mask.

**NOTE**: you cannot "SIGKILL" a single thread ID without killing all the TIDs
in the group (i.e. TGID or PID). Quoting `pthread_kill(3)` (implemented using
`tgkill()`):

>
> **Signals dispositions are process-wide**:
>
> - if a signal handler is installed, the handler is common for for all the
>   threads in the group.
>   What thread in the group run the handler? It's the thread (TID) that got
>   the signal. The handler execution is scheduled in the thread execution,
>   either waking the process from suspended state, or just scheduling the
>   handler along the normal program execution. The handler is invoked on the
>   thread stack (but i can also have a dedicate stack).
>
>   For a given signal different threads cannot have different handlers!

> - If the disposition of the signal is STOP, CONT, TERMINATE, this action
>   will affect all the threads of the process.
>

Similarly, you cannot send a signal causing a Term dispotion (such as SIGTERM)
to just one thread without causing all the threads in the group to exit. See
the next section for why.

### Term disposition

The term disposition causes `do_group_exit()` to be called on the target
process, unless the process has registered an handler for the signal.
I.e., it is equivalent to the process calling the `exig_group()` syscall,
without it cleanly terminating from user space point of view.
