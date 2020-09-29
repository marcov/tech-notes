# Linux Memory Map and Address Space

## 32-bit processors
- Address space limited to 32 bits, i.e. cannot directly address more than 4GB

Virtual addresses space for every processes (and for the kernel):
- [ 0x00000000 - 0xc0000000 - 1 ] -> user mode memory: 3GB
- [ 0xc0000000 - 0xffffffff   ] -> kernel mode memory: 1GB

Kernel is mapped in every process Virtual Address space, so that switching in/out
of kernel is fast (uses TLB).

So, if total system memory is <= 1GB: kernel mode can permanently map
all physical memory!

But if total system memory is > 1GB:
 - Physical addresses 0 - 869MB are always mapped in the (kernel mode) virtual
   addresses from [ 0xc0000000 - +869MB ] (ZONE_NORMAL)
   Here goes kernel data frequently accessed.
   These is also known as Low Memory

 - Physical addresses above 869MB are mapped on demand into (kernel mode) virtual
   [ -128MB - 0xffffffff ] (ZONE_HIGHMEM)
   This is mapped when need to access processes memory, page tables, etc...
   This is also known as High Memory

References:
- https://www.kernel.org/doc/Documentation/vm/highmem.txt

See also `/proc/PID/maps` and `/proc/PID/smaps`.

## 64-bit processors

Virtual address spaces are 64-bits wide, but only 48 bits are used.

- Bits [63:48] must be extension of bit 47, so either all 0 or all 1 (0xffff)
  So all adresses where this range of bits is not as that are invalid:
  0008000000000000 - ffff7fffffffffff

0000000000000000 - 00007fffffffffff (=47 bits) user space

------

ffff800000000000 - ffff87ffffffffff (=43 bits) guard hole, reserved for hypervisor
ffff880000000000 - ffffc7ffffffffff (=64 TB) direct mapping of all phys. memory
...
ffffffffff600000 - ffffffffff600fff (=4 kB) legacy vsyscall ABI
ffffffffffe00000 - ffffffffffffffff (=2 MB) unused hole
