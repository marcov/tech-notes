# Macros

## Why macro as a compound statement is bad
This would not compile:
    #define CODEBLOCK { int i; i = 0; i++; }

    if (condition)
        CODEBLOCK();
    else
        foobar();

So better use:
    #define CODEBLOCK do { int i; i = 0; i++; } while (0)

