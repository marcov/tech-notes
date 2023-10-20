# Undefined behaviour

## Pointers arithmetic
Undefined behaviour on pointer arithmetic. Use clang flags:

```
-fsanitize=undefined -Wnull-pointer-arithmetic
```

TLDR:

- NULL pointer arithmetic.
- the result of pointer arithmetic going beyond the boundary of an array (plus
  one).

## Data race

A data race is undefined behaviour. Data race TLDR: multiple threads accessing the same
data, with one of the access being a write.
