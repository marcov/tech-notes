# Arithmetic

- Using `((` `))`:
```
n=123
(( n+=1 ))
echo $n
#n=124
```

And also `echo $(( n+1 ))`

This construct can also be used to force a base, or trim leading zeroes:
- `$((10#0000123))` returns `123`. Without `10#` a number with leading zeroes
  could be interpreted as octal.

- Using `let`:
```
n=123
let n+=1
echo $n
#n=124
```

### **NOTE** about let

If the last ARG evaluates to 0, let returns 1; let returns 0 otherwise." ['help let']

So a better alternative for scripts with `set -e` is to use `(( ))`.
Otherwise let will just stop running the script silently!!!

```
let var=0
# $? = 1

let var++
# $? = 1

let var=1
# $? = 1

let var=2
# $? = 0

let var++
# $? = 0
```
