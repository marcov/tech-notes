Portability:
- ability to write a BPF program that works with different kernel version, where
kernel data structures are different.

Solutions:
a. Embed your BPF C program as string, and use BCC that builds the BPF on the fly
  using the kernel headers
Cons:
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
Missing #define Macros though :-(, but they can be found in `bpf_helpers.h`

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
