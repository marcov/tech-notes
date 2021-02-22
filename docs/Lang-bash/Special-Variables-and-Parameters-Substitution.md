# Special Variables and Parameters Substitution

`${@}`:  all parameters passed

`$$`: the PID of the currently running process

`$_`: the last parameter of the last command typed
E.g.
```
mkdir foobar
cd $_
# This will cd foobar
```

`!!`: recall last command typed
Eg.
```
# find . -name "*txt"
pippo.txt
```
`$(!!)`: recall the last command typed
Eg.
```
# find . -name "*txt"
pippo.txt
# vi $(!!) #  --> equivalent to: vi $(find . -name "*txt")
```

`$*`: All arguments separated by `$IFS`
`$@`: All arguments separated by ` `

```bash
fooStar() { echo "$*" }
fooAt() { echo "$@" }
IFS="x" fooStar 1 2 3 4
# 1x2x3x4
IFS="x" fooAt 1 2 3 4
# 1 2 3 4
```

## Parameters substitution

See also here: http://www.tldp.org/LDP/abs/html/parameter-substitution.html

`${variable:-value}`: if `variable` is set to a non-empty string, expands to `${variable}`, otherwise expands to `value`.

`${variable-value}`: if `variable` is set (also if set to empty string), expands to `${variable}`, otherwise expands to `value`.

`${variable:+value}`: if `variable` is set to a non-empty string, expands to `value`, otherwise expands to "".

`${variable+value}`: if `variable` is set (also if set to empty string), expands to `value`, otherwise expands to "".

`${variable#string}`: trim `string` **PREFIX** from `variable`.

`${variable%string}`: trim `string` **SUFFIX** from `variable`.

`${variable,,}`: **bash** Expands to lower case `${variable}`.
`${variable:l}`: **zsh** Expands to lower case `${variable}`.

`${variable^^}`: **bash** Expands to upper case `${variable}`.
`${variable:u}`: **zsh** Expands to upper case `${variable}`.

`${variable%pattern}`: Remove from `${variable}` the shortest pattern `${pattern}`.

`${variable%%pattern}`: Remove from `${variable}` the longest pattern `${pattern}`.

E.g.
```bash
var="foobar"
${var%o*r} # => fo : removes shortest "obar" pattern
${var%%o*r} => f : remove longer "oobar" pattern
```

`${variable/pattern/replacement}` : replace FIRST `pattern` with `replacement` in `${variable}`.
(If `replacement` is empty, just delete `pattern`).

`${variable/#pattern/replacement}` : like normal replace, but `pattern` is a **PREFIX** of
`${variable}`

`${variable/%pattern/replacement}` : like normal replace, but `pattern` is a **SUFFIX** of
`${variable}`

`${variable//pattern/replacement}` : replace ALL `pattern` with `replacement` in `${variable}`.
(If `replacement` is empty, just delete `pattern`).

`${variable:N:L}`: returns a slice of length `L` of `variable`, from offset `N`.
