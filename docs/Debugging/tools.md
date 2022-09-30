## Debugging tools

### rr

- Record failures, lets you replay them.
- Chaos mode to make intermittent bugs more reproducible.

### trace-cmd (ftrace)

Trace functions call in the kernel.

E.g.:

NOTE: if there's a fentry/fexit on the function call, it will not be shown!

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

### traceshark, kernelshark

Frontends for ftrace / perf.

### perf + hotspot

Capture and show flamegraph, call stack.

```console
$ sudo perf record --call-graph dwarf EXECUTABLE
$ hotspot perf.data
```

### Debugging stack

- `stacksize`
- `pstack`: dump the stack for all threads of a process
- `valgrind --tool=drd --show-stack-usage=yes`
