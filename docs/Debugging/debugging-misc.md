# Debugging misc

## Debugging stack

- `stacksize`
- `pstack`: dump the stack for all threads of a process
- `valgrind --tool=drd --show-stack-usage=yes`

## addr2line

From the man page:

    addr2line translates addresses into file names and line numbers.  Given an
    address in an executable or an offset in a section of a relocatable object,
    it uses the debugging information to figure out which file name and line
    number are associated with it.

    The executable or relocatable object to use is specified with the -e
    option.

E.g., if you only know the that an application `app-name` crashed at
`0x1234abcd` (by inspecting from crash dump/log), you can retrieve the
source code line with:

```console
$ addr2line -e app-name 1234abcd
/home/foo/app-src/main.c:567
```

## List of library dependencies of an executable

```
$ ldd [-v] <path_to_tool>
```

>
> NOTE: use wide option to get the symbols names printed.
>

Or:
```
$ readelf --wide -d <path_to_tool>
```

### List symbols used from specific libraries
```
$ readelf --wide -s <executable>
```

(E.g. symbols used from GLIBC):
```
$ readelf --wide -s <executable> | grep GLIBC*
```

## List of symbols

## Process Memory Map

Retrieve the memory map of a process:
```
$ sudo pmap <PID>
```

Show everything the kernel provides:
```
$ sudo pmap -XX <PID>
```
