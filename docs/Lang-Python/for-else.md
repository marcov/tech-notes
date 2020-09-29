# Python `for-else`

TLDR: else branch is executed if the `for` loop went thru all the items without `break`

Can be used in `for` loops, where the loop is _search-like_, i.e., it breaks on
a specific condition found in the loop.

E.g.
```py

def find(var):
    for v in range(5):
        if var == v:
            print('Found!')
            break
    else:
        print('Not found!')
```

```
find(3)
Found!
```

```
find(13)
Not found!
```
