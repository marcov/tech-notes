# Macros

## Why macro as a compound statement is bad

This does not compile:
```
#define CODEBLOCK() { int i; i = 0; i++; }

if (condition)
    CODEBLOCK();
else // error: ‘else’ without a previous ‘if’
    foobar();
```

Because the trailing `;` in `CODEBLOCK` separates the else from the previous if,
i.e.:
```
if (condition)
    { int i; i = 0; i++; };

else
{
    int foo;
}
```

So better use:
    #define CODEBLOCK do { int i; i = 0; i++; } while (0)

