# Libraries

> NOTE:
> Do not confuse linking with loading!

## Static Library (.a) - Statically Linked Library
A Library that is linked statically in an executable, i.e. the executable self
contains all the library symbols it needs to run.

## Shared Library (.so) - Dynamically Linked Library
Aka DSO - "Dynamic Shared Object(s)".
A library that is shared among different applications, i.e. it is loaded in memory
only one time for all the applications linked to it.

It is loaded by the kernel.

### Dynamic Linker

Used to load shared libraries. Aka `ld-linux` somewhere in `/lib/ld-linux.so.*`
You can invoke the linker as an executable, followed by an ELF file.

List all shared libraries resolution:
```
$ /lib64/ld-linux-x86-64.so.2 --list <path to executable>
```

Relevant variables:
- `LD_PRELOAD`: unconditionally preload the specified shared library, even if the
program did not request it.
This is done before actually loading the library the program requested.

- `LD_LIBRARY_PATH`: the path to look at when loading libraries, before looking into
system paths.

- `LD_DEBUG`: `LD_DEBUG=all <executable-name>` to show `ld` debug info while running
  an executable.

## Dynamically Loaded (DL) Library

Library that is loaded at runtime using `dlopen(...)`. This is useful when you
want to load at runtime some code in a library, like a plugin.

## PLT and GOT
PLT: Procedure Linkage Table. Stub of code that looks up for a shared library addresses
for functions in a table, called GOT: Global Offset Table.
>
> NOTE: addresses are actually stored / looked up in the .got.plt table!
>

### Example
Your code in `main()` is calling `getpid()`. The disassemble is:
```
0x0804845d <+25>:   call   0x8048350 <getpid@plt>
```

`getpid()` is a libc function, so the call is done going thru the PLT stub

PLT:
```
   0x08048350 <+0>:    jmp    *0x804a004
   0x08048356 <+6>:    push   $0x8
   0x0804835b <+11>:   jmp    0x8048330
```

The PLT is first trying to jump in the GOT entry for the function.

- If it's the first time getpid() is called, the GOT entry will just contain as
  address the instruction right after the jump.
  So the dynamic linker will do the lookup of the `getpid` name into the shared
  library, and store its address in the GOT entry.

- On subsequent calls to getpid, the GOT entry will contain the getpid address inside
  libc, so there will be no lookup :-)

### More Info

- [dynamic libraries tutorial](https://developer.ibm.com/tutorials/l-dynamic-libraries/)
- [LD preload tricks](http://www.goldsborough.me/c/low-level/kernel/2016/08/29/16-48-53-the_-ld_preload-_trick/)
- [PLT/GOT](https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html)

## LD Flags
### Start and end group
Used for tstatic libraries / archives only.
Wrap archives with `--start-group`, `--end-group` to allow specifying archives in
any order; references resolution done also for circular references.

## As needed / Not as needed
`--no-as-needed` is the default linking mode for shared libraries  =>
the library is always added as dependency (as shown by ldd), even if not used at
all.

`--as-needed` overrides default linking mode only include library as dependency if
it is actually needed / contains symbols needed by other objects.

## pkg-config
Given a library package name installed on the system, retrieve metadata about that library.
E.g.:
- it can be used to retrieve library compile and link flags.
```
$ pkg-config --cflags --libs uuid # uuid is the name of the library / name of the package containing the library
-I/usr/include/uuid -luuid
```
List all libraries packages name:
```
$ pkg-config --list-all
```

## ldconfig
Used to update the runtime linker cache (to speed up library lookup), and to handle
the links from ".so" to the actual libraries path.
It can also be used to retrieve the path of libraries on the system (--print-cache).

## ldd
Equivalent of `LD_DEBUG=libs <executable>`.

## vDSO (Virtual dynamic shared object)
Shared library that the kernel automatically loads into the process memory space.
It is used to map a subset of frequently used syscall, to avoid all of the overhead
of context switching:
- Only a very limited set of syscall is mapped (`gettimeofday`, `time`, ...)
- You can actually see the lib with `ldd binary-name` (`linux-vdso.so.1`)
- Library is built when you build the kernel. You can load symbols from it, as any
  other lib
