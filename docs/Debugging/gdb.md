# GDB

## Run command with a set of arguments

```
r [arguments you'd pass to the app under test]
```

Or, (**super useful trick**):

Just prefix you command line with `gdb --args`, and you  are good to go.

```console
$ gdb --args APP-NAME [APP-ARGUMENTS]

r
```

## Locals and arguments

```
info locals
info args
```

## Variables

### Symbol
Information about symbol for program counter

```
info symbol $pc
```

### Info on a global variable name

```
info variable <regex without quotes>
```

### Get the type

```
whatis var_name
```

## Breakpoints and Watchpoints

- Search for a function to break

```
# info functions <regex without quotes>
# E.g.:
info function ^get.*Async$
```

- Setting:

```
break fx | filename:linenumber
tbreak
watch variable_name | *0xADD1355
```

- Listing:

```
info breakpoints
info watchpoints
```

- Disabling (get the bkpt # with `info b`):

```
disable [bkpt #]
```

- Deleting (get the bkpt # with `info b`):

```
del[ete] [bkpt #]
```

- Delete all:

```
d[elete breakpoints]
```

- Conditional breakpoints:

```
b foobar.c:123 if  pVal == nullptr
```

or

```
b foobar.c:123
cond [brkpt # ] if  pVal == nullptr
```

## Call stack

### Backtrace

### Single thread

```
bt [thread #]
where
```

Full backtrace (code listing):

```
bt full
```

### All threads
```
thread apply all bt
```

### Stack frame
Go to a function in the backtrace (to get info about parameters,...)
```
frame [frame position #]
```

Resume execution from there:
```
fg
```

Print information on the variables for that frame:
```
info frame
```

## GDB server

- On target machine:
```
gdbserver localhost:1234 <myapp>
```

- On host (PC) machine
```
gdb
> target remote <IP>:1234
> continue....
>core <local-core-file>
```

## Get ELF infos

### Sections
```
maintenance info sections
```

## Use a separate symbol symbols file
```
add-symbol-file <debug-info-file> <address>
```

How to retrieve address?

Use the `Address` field for the `.text.` line from the output of:
```
readelf -WS <path-to-executable-without-debug>
```

Or, to automate that:
```
objdump -f <exec path> | grep  "start address" | sed -E "s/start address (0x[0-9a-f])/\1/g"
```

You can also use `objcopy` to include a symbol file name automatically looked up:
```
$ objcopy --add-gnu-debuglink=foobar-app.debug foobar-app
```

Read that using `objdump`:
```
$ objdump -g  foobar-app | grep debuglink -A 10
objdump: Warning: could not find separate debug file  ...
objdump: Warning: tried: /lib/debug/...
objdump: Warning: tried: /usr/lib/debug/...
objdump: Warning: tried: /home/marco/.debug/...
objdump: Warning: tried: .debug/...
objdump: Warning: tried: ...
Contents of the .gnu_debuglink section (loaded from foobar-app):

  Separate debug info file: foobar-app.debug
```

## Print data type format
Use `ptype`:
```
(gdb) ptype /o struct pc_packet
type = struct pc_packet {
/*    0      |     8 */    unsigned long length;
/*    8      |     0 */    unsigned char data[];

                           /* total size (bytes):    8 */
                         }
```

## Add a new directory path for looking up sources
```
directories /path/to/source/code/.../

dir /another/path/
```

Source files for which symbols have been read:
```
info sources
```

Set a directory mapping for sources:
```
set substitute-path /from/path /to/path
```

## Shared libraries
Info on the shared library loaded by the debugged application (load adddress ranges
and library path.
This includes both libraries loaded by ld (dynamic linker) and `dlopen()`'ed libraries.
```
info shared[library]
```

Match addresses of a shared libraries .so with the runtime addresses:

- `readelf -a lib.so` / `objdump -d lib.so` will provide relative addresses inside the library.
- The start address shown by GDB `info shared` is for the `.text` section inside the .so
- So, if GDB is showing address `0x00007ffffaaaabbb` for an instruction address,
  and library is loaded in the range `0x00007ffffaaaa000 - 0x00007ffffaaaafff`:
  * `0x00007ffffaaaabbb` - `0x00007ffffaaaa000` + `.text address` will give you
  the address inside the library as can be seen with `objdump -d` / `readelf`.

## Examine memory certain address
Disassemble at specific address:

(`$pc` stands for program counter register):
```
x/20i $pc - 10
```

Or also (`$rip` is the program counter register for x86-64):
```
x/20i $rip-10
```

## Reverse Execution
Enable recording:
```
record full
```

And then:
```
reverse-continue # or rc
reverse-step # or rs
reverse-stepi # or rsi
```

## Source code window
```
layout next
```
Or:
```
tui enable
```
```
tui disable
```

## Lock execution to a single thread

```
(gdb) help set scheduler-locking
Set mode for locking scheduler during execution.
off    == no locking (threads may preempt at any time)
on     == full locking (no thread except the current thread may run)
          This applies to both normal execution and replay mode.
step   == scheduler locked during stepping commands (step, next, stepi, nexti).
          In this mode, other threads may run during other commands.
          This applies to both normal execution and replay mode.
replay == scheduler locked in replay mode and unlocked during normal execution.
```

## Limit debug to a single thread

```
> break FooBar
...
# breakpoint met

> set scheduler-locking step
> # this will ignore breaks by other threads
```
## Following child on fork

If you want to follow the child process instead of the parent process, use the
command set follow-fork-mode.

```
set follow-fork-mode child
```
(the default is `parent` instead of `child`)

you can follow both with:

```
set detach-on-fork off
```
(the default is `on` instad of `off`)

Both processes will be held under the control of GDB. One process (child or
parent, depending on the value of follow-fork-mode) is debugged as usual, while
the other is held suspended.

## Kill process, but make it look like an accident

x86_64 version:

```console
$ gdb -p PID -batch -ex 'set {short}$rip = 0x050f' -ex 'set $rax=231' -ex 'set $rdi=0' -ex 'cont'
```

Explanation:

- `set {short}$rip = 0x050f`: write `0f 05` (i.e. syscall) at the location RIP
(program counter) is pointing to.
- `set $rax=231`: set RAX register to 231 (i.e. `__NR_exit_group` syscall number)
- `set $rdi=0`: set RDI register to 0 (i.e. 0 as syscall argument)

aarch64 version:

```console
$ gdb -p "$1" -batch -ex 'set {int}$pc = 0xd4000001' -ex 'set $w8=94' -ex 'set $x0=0' -ex 'cont'
```

Similar to x86, it calls `svc #0` instead of `syscall` with the right syscall number.
