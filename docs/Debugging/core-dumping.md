# Core Dumps

- Enable it:
```
ulimit -c unlimited
```

- Run your executable and make it crash:
```
./myapp
```

- [Depending on the system] Get the core dump with `coredumpctl`:
```
sudo coredumpctl list
sudo coredumpctl dump <identifier> > myapp.core
```

Or just: `sudo coredumpctl gdb <PID-of-crashed-app>`

- Load the core-dump into GDB:
```
gdb ./myapp
core-file <core-file>
```
Or just: `gdb ./myapp core.####`
