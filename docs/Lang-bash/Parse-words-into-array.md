# Parse words into array
Mind the quotes, works only in bash:
```
read -r -a arrayName <<< "$(cmd)"
```

Array size: `${#arrayName[@]}`
