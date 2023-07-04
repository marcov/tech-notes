# BPF (eBPF)

## Main Goals

Portability:

- ability to write a BPF program that works with different kernel version,
  where kernel data structures are different.

Solutions:

a. Embed your BPF C program as string, and use BCC that builds the BPF on the fly
  using the kernel headers
CONS:

- LLVM is a big binary,
- resource-heavy,
- slow,
- needs kernel headers installed,
- compilation errors are only found at runtime.

b. CO-RE. Components:

- BTF type information
- Clang able to use write BTF relocations
- libbpf (user space BPF loader library): adjust BPF compiled code to the specific
  kernel version using BTF info
- kernel

## BTF

Format to describe the type information of C programs. Compact size.
Exposed via `/sys/kernel/btf/vmlinux`; and can be read via bpftool, getting all
the kernel types, as if we had the kernel headers.

```
$ bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h
```

Your BPF program can just include a single `vmlinux.h` file.
Missing `#define` macros though :-(, but they can be found in `bpf_helpers.h`

## Clang

Clang support generating BPF programs with BTF relocation information, so that
the BPF loader can adjust the program at runtime for the particular kernel it
is running on. -> Field offset relocation.

## BPF loader (libbpf)

BPF program loader. It takes a BPF ELF object file, post-processes it, setups various
kernel objects and triggers BPF program loading and verification.

Resolved and matches all types and fields.

## Kernel

No specific kernel support required, if BTF is exposed, the BPF program can be loaded
as a traditional BPF one.

## Type of BPF Programs & Probes

See `/sys/kernel/debug/tracing/events/...` and `/sys/kernel/debug/tracing/available_events`.

- tracepoints / raw tracepoints (includes any syscall enter / exit).
- `kprobe` / `kretprobe`: any kernel func
- `fentry` / `fexit`: any kernel func (need trampoline support for the architecture!)
- LSM: LSM hooks in "security.h"
- perf_events (used by BPF program type perf event)
- `fmod_ret`: override UM function and syscalls return code. E.g. return a
  syscall error or a fake int result.
  * can only be hooked to a "security_" prefixed function.
- `bpf_iter`: iterator over various stuff, e.g. list of all current task structures.
- `syscall`: a program that can call sycalls.

>
> From `libbpf-bootstrap`:
>
> The big distinction between fexit and kretprobe programs is that fexit one
> has access to both input arguments and returned result, while kretprobe can
> only access the result.
>

If you hook on exit path using `kretprobe`, you may not be able to retrieve the
function arguments. The registers holding the arguments at the function entry
could be clobbered by the function execution. However this _should_ not happen
with `fexit`, according to `BPF_PROG` documentation in `bpf_tracing.h`

## Useful helper functions

- `bpf_get_current_pid_tgid`: returns PID / TGID of a thread.
- `bpf_d_path`:  returns full path for given **struct path** object.
   **NOTE**: it is only allowed in a set of functions, see `btf_allowlist_d_path`
   in the kernel code.
- `bpf_send_signal`: raises a signal on the current thread.

Rootkit - oriented:

- `bpf_probe_write_user`: Writes the memory of a user space thread (subject to
  TOC-TOU limitations). It can corrupt user memory!

- `bpf_override_return`:

  * Only for kernel functions defined with `ALLOW_ERROR_INJECTION(...)`
  * Needs a kernel with `CONFIG_BPF_KPROBE_OVERRIDE`
  * used at entry: syscall completely skipped!
  * used at exit: alters a syscall return value, but the syscall is executed.

`bpf_probe_read_user() / bpf_probe_read_user_str() / bpf_probe_write_user()`:
read / write an argument from a syscall, or read an VM addres of a user space
program. The address can be also passed via `skel->bss->ptr`.

`bpf_copy_from_user()`: sleepable version of `bpf_probe_read_user()`. Can only
be used in sleepable BPF progs.

## List BPF stuff

List of BPF programs:

```
$ bpftool prog
```

List of BPF maps:

```
$ bpftool map
```

List of all BTF info, including functions: `bpftool btf dump file
/sys/kernel/btf/vmlinux format raw`

Can you hook to `FUNCTION_NAME`?

```
bpftool btf dump file /sys/kernel/btf/vmlinux | grep FUNCTION_NAME
```

## Pinning BPF programs

Normally, a BPF program requires the program that loaded it to be running, in
order for the program to be kept loaded in the kernel. Alternatively, a BPF
program can be pinned to a file under the special filesystem `bpffs`.

## Interpreting verifier errors

See the kernel file `kernel/bpf/verifier.c : reg_type_str[]`:

```c
[NOT_INIT] = "?",
[SCALAR_VALUE] = "inv",
[PTR_TO_CTX] = "ctx",
[CONST_PTR_TO_MAP] = "map_ptr",
[PTR_TO_MAP_VALUE] = "map_value",
[PTR_TO_MAP_VALUE_OR_NULL] = "map_value_or_null",
[PTR_TO_STACK] = "fp",
[PTR_TO_PACKET] = "pkt",
[PTR_TO_PACKET_META] = "pkt_meta",
[PTR_TO_PACKET_END] = "pkt_end",
[PTR_TO_FLOW_KEYS] = "flow_keys",
[PTR_TO_SOCKET] = "sock",
[PTR_TO_SOCKET_OR_NULL] = "sock_or_null",
[PTR_TO_SOCK_COMMON] = "sock_common",
[PTR_TO_SOCK_COMMON_OR_NULL] = "sock_common_or_null",
[PTR_TO_TCP_SOCK] = "tcp_sock",
[PTR_TO_TCP_SOCK_OR_NULL] = "tcp_sock_or_null",
[PTR_TO_TP_BUFFER] = "tp_buffer",
[PTR_TO_XDP_SOCK] = "xdp_sock",
[PTR_TO_BTF_ID] = "ptr_",
[PTR_TO_BTF_ID_OR_NULL] = "ptr_or_null_",
[PTR_TO_PERCPU_BTF_ID] = "percpu_ptr_",
[PTR_TO_MEM] = "mem",
[PTR_TO_MEM_OR_NULL] = "mem_or_null",
[PTR_TO_RDONLY_BUF] = "rdonly_buf",
[PTR_TO_RDONLY_BUF_OR_NULL] = "rdonly_buf_or_null",
[PTR_TO_RDWR_BUF] = "rdwr_buf",
[PTR_TO_RDWR_BUF_OR_NULL] = "rdwr_buf_or_null",
```

If loading bpf code results in this error, it means you are attempting to read
a (relocatable) structure field that your kernel does not have (or better said,
cannot relocate):

```
180: (85) call unknown#195896080
invalid func unknown#195896080
```

## BPF iterator

- Declare the program with SEC("iter/task"). See kernel code for all possible `"iter/hook"`
  type of iterators.
- seq write
- iter attach
- Need to read seq fd to make the iterator run.

Alternatively, can use pin the iterator to a bpffs file path:

- Read from the path to run the iterator.
- Delete the file path to unload the iterator program.

## BPF tail call

- Tail called programs must be of the same type of the caller.
  You have the option to declare the tail called BPF program to be of the same type,
  or leave a BPF program with a generic type, and use the helper functions
  `bpf_program__set_xxx()` to set a type before loading the program.
- They also need to match in terms of JIT compilation, thus either JIT compiled or
  only interpreted programs can be invoked, but not mixed together.
- BPF tail call functions are paired with an prog array map used as jump table
  (BPF_MAP_TYPE_PROG_ARRAY).
  Each entry of the map is a program fd. UM needs to configure it before loading the
  program. When BPF jumps to a tail call functions, it jumps to a fd #:
  `bpf_tail_call(ctx, &array_map_of_fds, __fd_number__);`
- The context `ctx` passed to `bpf_tail_call`, must be really a pointer to a context,
  it cannot be any pointer to a argument the user wants to pass around.

## JIT

JIT compilers speed up execution of the BPF program significantly since they
reduce the per instruction cost compared to the interpreter.
Often instructions can be mapped 1:1 with native instructions of the
underlying architecture.

- Dynamic enable / disable is controlled with `/proc/sys/net/core/bpf_jit_enable`.
- Permanently enable: `CONFIG_BPF_JIT_ALWAYS_ON`.

## Maps

### Memory mapped

You can memory maps a BPF map of type array. Declare the map with `BPF_F_MAPPABLE`.
A limitation is that the map __cannot be read only from UM__, i.e. declared
with `BPF_F_RDONLY`.

### Map of maps

Limitations: you can only create a new inner map from UM.

## BPF Links

A `bpf_link` is an abstraction used to:

- represent an attachment of a BPF program to a BPF hook point;
- encapsulate ownership of an attached BPF program to a process, or to a file path
  (via BPFFS). This allows to survive a user process exit.
See: https://lore.kernel.org/bpf/20200228223948.360936-1-andriin@fb.com/

## BPF spinlocks

Used to mutex access/updates to a single map element.

## CORE

Thanks to CORE you can write bpf code that supports different structure formats
for the different kernel version. But, make sure to declare any alternative
version of a default struct foobar (defined in vmlinux.h ), as struct
`foobar___v1`, struct `foobar___v2` with **exactly 3** underscores!

Quoting some libbpf code in the kernel:

```
 * 1. For given local type, find corresponding candidate target types.
 *    Candidate type is a type with the same "essential" name, ignoring
 *    everything after last triple underscore (___). E.g., `sample`,
 *    `sample___flavor_one`, `sample___flavor_another_one`, are all candidates
 *    for each other. Names with triple underscore are referred to as
 *    "flavors" and are useful, among other things, to allow to
 *    specify/support incompatible variations of the same kernel struct, which
 *    might differ between different kernel versions and/or build
 *    configurations.
```

Use `bpf_core_field_exists()` to select what of the struct to use to read data.

## Nice helpers

- `bpf_get_stackid`: save the user space or kernel space functions call stack
  into a map.

## Direct memory read

Some program types (tracing and trampolines) allows direct memory reads of
kernel pointers, without having to use `bpf_probe_*` helpers.

However, you still need to have the compiler emit CO-RE relocations, either
using `__builtin_preserve_access_index`, or by tagging a kernel struct
definition with `__attribute__((preserve_access_index))` - these twos are
equivalent.

## Programs statistics

Write `1` to `/proc/sys/kernel/bpf_stats_enabled`.

That will make bpftool show additional info:

- run_cnt: the number of times the program was executed.
- run_time_ns: the **cumulative** program execution time in nanoseconds
  including the off-cpu time when the program was sleeping.

```
sudo bpftool prog show

--- CUT ---
3001: raw_tracepoint  name my_tracepoint  tag abcdef0123456789  gpl run_time_ns 41752 run_cnt 24

--- CUT ---
```

Stats in newer kernel:

- verified_insns: the number of verifier processed instructions - what's
  currently dumped in the libbpf log on program load, when the log level is
  verbose enough.

- recursion_misses: how many times recursion was prevented (TBD).
