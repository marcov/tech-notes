# Core dumps

- Enable it:

```console
$ ulimit -c unlimited
```

- How and where to write a coredump is configured in
  `/proc/sys/kernel/core_pattern`. See `core(5)` for details.

- Run your executable and make it crash:

```
$ ./myapp
```

- If you system is configured to manage core dump with `coredumpctl`:

```console
$ sudo coredumpctl list
$ sudo coredumpctl dump <identifier> > myapp.core
```

Or just: `sudo coredumpctl gdb <PID-of-crashed-app>`

- Load the core-dump into GDB:

```console
$ gdb ./myapp
$ core-file <core-file>
```

Or just: `gdb ./myapp core.####`
