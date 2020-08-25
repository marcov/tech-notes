# Division with ceiling

NOTE: could overflow!
```c
#define DIV_CEIL(dividend, divisor) \
                ((dividend) + (divisor) - 1) / (divisor)
```
