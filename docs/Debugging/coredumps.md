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

## Pairing a coredump with a binary & debug files

There _should_ be a "Build ID" stored in executables & debug files. You can
obtain it e.g. with `readelf -a` and compare it with the ID in the corefile.

```console
$ readelf -a /usr/bin/python3

[ -- CUT -- ]
Displaying notes found in: .note.gnu.build-id
  Owner                Data size        Description
  GNU                  0x00000014       NT_GNU_BUILD_ID (unique build ID bitstring)
    Build ID: 08d0fd215a9a98d5333fda7e5a9a46c923148415
```

Generate a coredump from it and verify the build ID to match:

```
$ ulimit -c unlimited
$ echo '/tmp/core.%e.%P' | sudo tee /proc/sys/kernel/core_pattern
$ /usr/bin/python3 -c 'import os; os.abort()'

$ eu-unstrip -n --core /tmp/core.python3.1054277.1054277
0x55e0ca3e5000+0x5e8000 08d0fd215a9a98d5333fda7e5a9a46c923148415@0x55e0ca3e5378 . - /usr/bin/python3.10
0x7fffd2d5e000+0x1000 9483b2083c2a30ba4e4f346b36803f814b9a1743@0x7fffd2d5e540 . - linux-vdso.so.1
0x7f5de5358000+0x3b2d8 15921ea631d9f36502d20459c43e5c85b7d6ab76@0x7f5de53582d8 /lib64/ld-linux-x86-64.so.2 /usr/lib/debug/.build-id/15/921ea631d9f36502d20459c43e5c85b7d6ab76.debug ld-linux-x86-64.so.2
0x7f5de4e00000+0x228e50 c289da5071a3399de893d2af81d6a30c62646e1e@0x7f5de4e00390 /lib/x86_64-linux-gnu/libc.so.6 /usr/lib/debug/.build-id/c2/89da5071a3399de893d2af81d6a30c62646e1e.debug libc.so.6
0x7f5de520b000+0x1b0b8 30840b79ac329ecbf1dec0bb60180eed256d319f@0x7f5de520b2d8 /lib/x86_64-linux-gnu/libz.so.1 - libz.so.1
0x7f5de5227000+0x300b8 d212d1f61d04a1e60fccad1a8c118428cfd9be42@0x7f5de52272d8 /lib/x86_64-linux-gnu/libexpat.so.1 - libexpat.so.1
0x7f5de5258000+0xe6108 a88ef0199bd5e742ebd0c359edf5cb2be0ec08b5@0x7f5de52582e8 /lib/x86_64-linux-gnu/libm.so.6 /usr/lib/debug/.build-id/a8/8ef0199bd5e742ebd0c359edf5cb2be0ec08b5.debug libm.so.6
```
