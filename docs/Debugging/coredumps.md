# coredump files

Certain signals cause a process to terminate and produce a core dump file.
They are (but refer to `signal(7)` for an accurate list):

- SIGABRT
- SIGBUS
- SIGFPE
- SIGILL
- SIGIOT
- SIGQUIT
- SIGSEGV
- SIGSYS
- SIGTRAP
- SIGUNUSED
- SIGXCPU
- SIGXFSZ

Of course, if you change the signal default action to something else, no
coredump is generated.

To make sure a coredump file, is always produced, set its file size to
unlimited:

```console
$ ulimit -c unlimited
```

How and where Linux writes a coredump is configured in `/proc/sys/kernel/core_pattern`.
See `core(5)` for the format.

Simple example format: `/tmp/core.%e.%P`. Make sure the process has write
permissions at that location.

## coredumpctl

You system may be configured to manage coredump with `coredumpctl`. If so,
coredumps are listed here:

```console
$ sudo coredumpctl list
$ sudo coredumpctl dump <identifier> > myapp.core
```

Or just: `sudo coredumpctl gdb <PID-of-crashed-app>`

Load the coredump into GDB:

```console
$ gdb ./myapp
$ core-file <core-file>
```

Or just: `gdb ./myapp core.####`

