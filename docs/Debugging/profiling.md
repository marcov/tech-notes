# Linux Software Profiling

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

## perf + hotspot

Capture and show flamegraph, call stack.

```console
$ sudo perf record --call-graph dwarf EXECUTABLE
$ hotspot perf.data
```

## mpstat

Processor related statistics.

```
$ mpstat 1
```

## pprof

TBD. Frontend for perf and other profiling data files.

