# C macros, token pasting, stringification

Problem:
- you want a macro to obtain a string / another macro name.
- the macro uses token pasting to replace a token with a string.

What you may do is:
```
#define MY_PINNUM  3
#define GET_PIN_NAME(num)      PIN_##num
```

And by using it with `GET_PIN_NAME(MY_PINNUM)` you would expect to get `PIN_3`.
BUT you will obtain as expansion `PIN_MY_PINNUM`, because `MY_PINNUM` is used
straight away as a string (**stringification**) and not as a macro to be expanded.

So to get the proper expansion it is sufficient to pass through an intermediate macro that will take care of the actual expansion:
```
#define MY_PINNUM  3
#define GET_PIN_NAME(num)      PIN_NAME_(num)
#define PIN_NAME_(numstr)      PIN_##numstr
```

In this case `GET_PIN_NAME(MY_PINNUM)` will give you `PIN_3`.

More details:
https://gcc.gnu.org/onlinedocs/cpp/Stringification.html
