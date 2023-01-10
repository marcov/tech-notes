## malloc, fork, and free

This is flagged as a leak by both the leak sanitizer and valgrind.
But it is not when replacing `return 0` with `exit()` or `_exit()`.

Apparently that's because in the former case `mem` goes out of scope, while in
the latter case it does not.

```c
int main(void) {
    uint8_t mem = malloc(4096);

    return 0;   // A leak when returning,
    // exit(0); // but not a leak when calling exit.
}
```

## Forking after malloc

Heap allocations are copied-on-write for the child. Hence, the child needs to
follow the same rules for freeing mem as the parent.

The differences b/w `return` vs `exit` still apply.

```c
int main(void) {
    uint8_t mem = malloc(4096);

    if (fork() == 0) {
        return 0;   // A leak

        // _exit(0); // not a leak

        // free(mem);
        // return 0; // obviously not a leak.
    }

    free(mem);
    return 0;   // A leak when returning,
    // exit(0); // but not a leak when calling exit.
}
```
