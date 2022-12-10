# Notes on the Linux Programming Interface

## How To Call a Syscall

-  Use `syscall()`:

```c
syscall(SYS_kill, pid, signum);
```

- Use inline asm:

```c
//
// 57 is the syscall number for fork()
// the return value is stored in the pid variable
//
int pid;
asm("mov    $57, %%eax\n syscall\n" : "=r" (pid));
```

## File System
```
filename -> inode identifier -> inode reference
                                 / | \
                                /  |  \
                               /   |   \
                        [data0] [data1] [data2] ...
```

### inode
- Unique identifier for a file object.
- File metadata

### dentry
Translates between file name and inode. There is a cache for both dentries and
inodes.

## select() vs. poll()
TL;DR: Use `poll()` instead of `select()`
Reasons:
 - select() has poor performances (for-loop from FD 0 to target FD).
 - select() can destroy your stack, if checking for a FD larger than FD_SETSIZE.

More info: https://beesbuzz.biz/code/5739-The-problem-with-select-vs-poll
