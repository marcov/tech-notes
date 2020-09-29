# Return Codes

### `$()`
`$()` propagates the return code to the caller.

    $ foo=$(false)
    $ echo $?
    1

Beware that if you use `local` the errcode is masked!

    $ local foo=$(false)
    $ echo $?
    0

### Inside functions
To have the error code propagate, make the last command fail before returning:
    $ foo() { false; return; }
    $ foo
    1

This does not propagate the error:
    $ bar() { if [ "1" != "0" ]; then return; fi }
    $ bar
    $ echo $?
    0

