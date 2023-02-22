# Linux Tracing Technologies

More info: https://jvns.ca/blog/2017/07/05/linux-tracing-systems/#kprobes

|       | Kernel      | User                |
|-------|-------------|---------------------|
|Static | tracepoints | USDT / dtrace probes|
|Dynamic| kprobes     | uprobes             |

## Kprobes / uprobes (dynamic)

- kprobe: dynamic instrumentation of kernel: zero overhead when not in use.
  Can hook entry and exit of any kernel function
  Dynamically change the kernel code at runtime to trace when a given
  kernel function is called.
  It may not page fault or sleep.
  It runs with interrupts disabled.

- uprobe: equivalent of kprobe in user space

## Tracepoint (static)

- Kernel code compiled with a predefined set of hook functions around salient
  kernel functionalities.

  You can register a function (a probe) to be called when hitting any of these
  hooks.

  More efficient than kprobes: the probe execution check is only a compare and
  branch.

Like kprobes it may not page fault or sleep.

### List of available tracepoints

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

## eBPF

Extension to cBPF:

- Adds ability to call in-kernel helper functions
- Adds shared data structures used for storage (maps)

(limited) C -(cLang)-> eBPF bytecode -(JIT compiler)-> machine code

## DTrace

- Dynamic tracing framework
- Never made it to upstream Linux kernel
- https://www.cs.princeton.edu/courses/archive/fall05/cos518/papers/dtrace.pdf
