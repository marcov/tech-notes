## Debugging tools

### rr

- Record failures, lets you replay them.
- Chaos mode to make intermittent bugs more reproducible.

### trace-cmd (ftrace)

Trace functions call in the kernel.

E.g.:

NOTE: if there's a fentry/fexit on the function call, it will not be shown!

```console
# trace-cmd record -p function_graph -g copy_mnt_ns -O nofuncgraph-irqs -F unshare -m /bin/true
# trace-cmd report | less
```

https://www.youtube.com/watch?v=JRyrhsx-L5Y

### traceshark, kernelshark

Frontends for ftrace / perf.

### perf + hotspot

Capture and show flamegraph, call stack.

```console
$ sudo perf record --call-graph dwarf EXECUTABLE
$ hotspot perf.data
```
