# Range arrays, for loops

- Using braces expansion
> NOTE:
> - you CANNOT specify a range using variables.
> - upper value included

```
for i in {1..10}; do
  echo $i
done
```

- Using `seq`:
> NOTE:
> - you CAN specify a range using variables.
> - upper value included

```
for i in $(seq 0 ${max}); do
  echo $i
done
```

- Using C-style for loops:
```
nCtrs=$( ... )
for (( i=1; i<=$nCtrs; i++ )); do
  echo $i
done
```
