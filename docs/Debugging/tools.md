# Debugging & Tracing Tools

## rr

- Record failures, lets you replay them.
- Chaos mode to make intermittent bugs more reproducible.

## trace-cmd (ftrace)

Trace functions call in the kernel. E.g.:

>
> NOTE: if there's a fentry/fexit on the function call, it will/may not be shown?
>

Run a command and capture all its kernel functions calls:

```console
# trace-cmd record -p function_graph -O nofuncgraph-irqs -F unshare -m /bin/true
# trace-cmd report | less
```

Capture a specific kernel function (and all functions it calls), for any process:

```console
# trace-cmd record -p function_graph -O nofuncgraph-irqs -g __x64_sys_lseek
```

`-F` and `-g` options can be used together.

https://www.youtube.com/watch?v=JRyrhsx-L5Y

## traceshark, kernelshark

Frontends for ftrace / perf.

## systemtap

Dynamic kernel instrumentation, by building and loading a kernel module at runtime.
Using kprobes, uprobes, USDT.

Can get both userspace and kernel info.

See:

- https://wiki.debian.org/SystemTap
- https://www.sourceware.org/systemtap/wiki/

Hello world example:

```console
$ stap -v -e 'probe oneshot { println("hello world") }'
```

## perf + hotspot

Capture and show flamegraph, call stack.

```console
$ sudo perf record --call-graph dwarf EXECUTABLE
$ hotspot perf.data
```

## strace

- Trace system calls
- Uses ptrace

Filtering by system call name:

```
strace -e trace=read,write,stat,openat
```

Useful options:

- `--trace='!mprotect,mmap,close,brk'`: specify what syscalls not to trace.
- `e expr`: which event to trace, e.g. only specific syscalls.
- `-f`: trace child processes as they are created
- `-v`: print unabbreviated stuff
- `-s 1024`: maximum string size to print
- `--decode-fds=path`: print path names along with fd number

**NOTE**: Apparently, you cannot run setuid binaries with strace.

## bpftrace

New gen tracing tool inspired by DTrace, using eBPF.

Print kernel stack trace:

```console
$ sudo bpftrace -e 'kprobe:icmp_echo { print(kstack); }'

# in another term
$ ping localhost
```

## bcc

Wrapper for `bpf()` syscall (BPF_PROG_LOAD).

## ltrace

- Trace library calls
- Uses ptrace

## perf

- Found in the kernel source tree at "/tools/perf" (package: "linux-tools")
- Kernel profiling & sampling, statistics
- Sample first, analyze later
- Can instrument tracepoints, kprobes, uprobes, USDT probes.

E.g.: `sched_process_exec` is a tracepoint.  Print # of exec'ed process every 1s:
```
$ perf stat -e sched:sched_process_exec -I 1000
```

- List sched tracepoints with `sudo perf list "sched:*"`
- List all tracepoints with `sudo perf list | grep -i tracepoint`

Get call-graph and other stuff for a PID (can be paired with flame graph generator):
```
sudo perf record -F max -ag -p PID
#... let processes run for a while, then ctrl-c
sudo perf report --stdio
```

## pprof

TBD. Frontend for perf and other profiling data files.
