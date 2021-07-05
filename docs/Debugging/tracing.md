# Linux Tracing

More info: https://jvns.ca/blog/2017/07/05/linux-tracing-systems/#kprobes

Dynamic instrumentation (BPF, DTrace)
- Zero overhead when not in use

## Tools

### bpftrace
- New gen tracing tool inspired by DTrace, using BPF.

### DTrace
- Dynamic tracing framework
- Never made it to upstream Linux kernel
- https://www.cs.princeton.edu/courses/archive/fall05/cos518/papers/dtrace.pdf

### ltrace
- Trace library calls
- Uses ptrace

### perf
- Kernel profiling & sampling, statistics
- Sample first, analyze later
- Can instrument tracepoints, kprobes, uprobes, USDT probes.

E.g.: `sched_process_exec` is a tracepoint.  Print # of exec'ed process every 1s:
```
$ perf stat -e sched:sched_process_exec -I 1000
```

- List sched tracepoints with `sudo perf list "sched:*"`
- List all tracepoints with `sudo perf list | grep -i tracepoint`

### strace
- Trace system calls
- Uses ptrace
Filtering by system call name:
```
strace -e trace=read,write,stat,openat
```

## Technology

## Probes (dynamic)
- kprobe: dynamic instrumentation of kernel
  Dynamically change the kernel code at runtime to trace when a given instruction
  is called
- uprobe: equivalent of kprobe in user space

### Tracepoint (static)
- Kernel code can call hook functions, called probes.
- Connect a probe to a tracepoint: the hook calls the probe.
- See https://www.kernel.org/doc/Documentation/trace/tracepoints.rst

#### List of available tracepoints

For each tracepoint you have a subdir with the format
```
$ sudo ls /sys/kernel/debug/tracing/events/
```

Or:
```
$ sudo tplist
```

Or:
```
$ sudo perf --list tracepoint
```

### BPF
|       | Kernel      | User                |
|-------|-------------|---------------------|
|Static | tracepoints | USDT / dtrace probes|
|Dynamic| kprobes     | uprobes             |

eBPF
Extension to cBPF:
- Call in-kernel helper functions
- access shared data structures (eBPF maps)

(limited) C -(CLang)-> eBPF bytecode -(JIT compiler)-> machine code

bcc
Wrapper for `bpf()` syscall (BPF_PROG_LOAD).
