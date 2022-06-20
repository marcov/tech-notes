# EBPF

## Main Goals

Portability:
- ability to write a BPF program that works with different kernel version, where
kernel data structures are different.

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
Clang support generating BPF programs with BTF relocation information, so that the
BPF loader can adjust the program at runtime for the particular kernel it is running on.
-> Field offset relocation.

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
- kprobes / kretprobes: any kernel func
- `fentry` / `fexit`: any kernel func
- LSM: LSM hooks in "security.h"
- perf_events (used by BPF program type perf event)
- `fmod_ret`: override UM function and syscalls. Returns an error or a fake result.
- `bpf_iter`: iterator over various stuff, e.g. list of all currecnt task structures.


## Useful helper functions
- `bpf_get_current_pid_tgid`: returns PID / TGID of a thread.
- `bpf_d_path`:  returns full path for given **struct path** object.
   **NOTE**: it is only allowed in a set of functions, see `btf_allowlist_d_path`
   in the kernel code.
- `bpf_send_signal`: raises a signal on the current thread.

Rootkit - oriented:
- `bpf_probe_write_user`: Writes the memory of a user space thread (subject to TOC-TOU limitations).
  It can corrupt user memory!

- `bpf_override_return`:
 * used at entry: syscall completely skipped!
 * used at exit: alters a syscall return value, but the syscall is executed.

`bpf_probe_read_user() / bpf_probe_read_user_str() / bpf_probe_write_user()`:
read / write an argument from a syscall, or read an VM addres of a user space program.
The address can be also passed via `skel->bss->ptr`.

`bpf_copy_from_user()`: sleepable version of `bpf_probe_read_user()`. Can only be
used in sleepable BPF progs.

## List BPF stuff
List of BPF programs:
```
$ bpftool prog
```

List of BPF programs:
```
$ bpftool map
```

List of all BTF info, including functions:
`bpftool btf dump file /sys/kernel/btf/vmlinux format raw`

## Pinning BPF programs
Normally, a BPF program requires the program that loaded it to be running, in order
for the program to be kept loaded in the kernel.
Alternatively, a BPF program can be pinned to a file under the special filesystem
`bpffs`.

## Interpreting verifier errors
See the kernel file `kernel/bpf/verifier.c`:

```
/* string representation of 'enum bpf_reg_type' */
static const char * const reg_type_str[] = {
	[NOT_INIT]		= "?",
	[SCALAR_VALUE]		= "inv",
	[PTR_TO_CTX]		= "ctx",
	[CONST_PTR_TO_MAP]	= "map_ptr",
	[PTR_TO_MAP_VALUE]	= "map_value",
	[PTR_TO_MAP_VALUE_OR_NULL] = "map_value_or_null",
	[PTR_TO_STACK]		= "fp",
	[PTR_TO_PACKET]		= "pkt",
	[PTR_TO_PACKET_META]	= "pkt_meta",
	[PTR_TO_PACKET_END]	= "pkt_end",
	[PTR_TO_FLOW_KEYS]	= "flow_keys",
	[PTR_TO_SOCKET]		= "sock",
	[PTR_TO_SOCKET_OR_NULL] = "sock_or_null",
	[PTR_TO_SOCK_COMMON]	= "sock_common",
	[PTR_TO_SOCK_COMMON_OR_NULL] = "sock_common_or_null",
	[PTR_TO_TCP_SOCK]	= "tcp_sock",
	[PTR_TO_TCP_SOCK_OR_NULL] = "tcp_sock_or_null",
	[PTR_TO_TP_BUFFER]	= "tp_buffer",
	[PTR_TO_XDP_SOCK]	= "xdp_sock",
	[PTR_TO_BTF_ID]		= "ptr_",
	[PTR_TO_BTF_ID_OR_NULL]	= "ptr_or_null_",
	[PTR_TO_PERCPU_BTF_ID]	= "percpu_ptr_",
	[PTR_TO_MEM]		= "mem",
	[PTR_TO_MEM_OR_NULL]	= "mem_or_null",
	[PTR_TO_RDONLY_BUF]	= "rdonly_buf",
	[PTR_TO_RDONLY_BUF_OR_NULL] = "rdonly_buf_or_null",
	[PTR_TO_RDWR_BUF]	= "rdwr_buf",
	[PTR_TO_RDWR_BUF_OR_NULL] = "rdwr_buf_or_null",
};
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

## BPF spin locks
Used to mutex access/updates to a single map element.

