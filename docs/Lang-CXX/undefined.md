# Undefined behaviour

## Pointers arithmetic

Undefined behaviour on pointer arithmetic. Use clang flags:

```
-fsanitize=undefined -Wnull-pointer-arithmetic
```

TLDR:

- Null pointer arithmetic.

    If p is a null pointer to an object type, the C expression p + 0 always
    evaluates to p on modern hosts, even though the standard says that it has
    undefined behavior.

- the result of pointer arithmetic going beyond the boundary of an array (plus
  one).

## Data race

A data race is undefined behaviour. Data race TLDR: multiple threads accessing the same
data, with one of the access being a write.

## Reading uninitialized variables.

Reading uninitialized variables is undefined behaviour.
