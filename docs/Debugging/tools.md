# Debugging, Performance & Tracing Tools

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

Log whenever one or more function is called system-wide:

```console
# trace-cmd record -p function -l inet_recvmsg -l inet6_recvmsg -l inet_sendmsg -l inet6_sendmsg
```

Log whenever a specific kernel function (and all its call stack), for any process:

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

Hook using trampolines:
```console
sudo bpftrace -e 'kretfunc:inet_release { printf("%s: ret: %lx, stack: %s\n", probe, retval, kstack);}'
```

Get all hookable functions with:

```console
sudo bpftrace -l
```

Note: it's only showing kfunc and kfunc, but probes can also be set on
`kretfunc` and `kretprobe`.

## bcc

Wrapper for `bpf()` syscall (BPF_PROG_LOAD).

## ltrace

- Trace library calls
- Uses ptrace

