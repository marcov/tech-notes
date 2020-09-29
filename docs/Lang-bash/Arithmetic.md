# Arithmetic

- Using `((` `))`:
```
n=123
(( n+=1 ))
echo $n
#n=124
```

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
