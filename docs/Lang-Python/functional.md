# Python functional programming

## Filter a dictionary by key or value

```
# Unluckily you cannot unpack a tuple in lambdas ...

envs = filter(lambda item: item[0] in ('USER','HOME', 'PWD'), os.environ.items())

dict(envs) # Get a dictionary
next(envs) # Get the next element.
```

## `reduce()`: apply a function _cumulatively_ to a list

E.g., an equivalent of `sum()` is:
```
from functools import reduce
reduce(lambda x,y: x+y, [1,2,3,4])
```

## `map()`: apply a function to _each_ element of a list

```
list(map(lambda x: 2**x, [1,2,3,4]))
```
