# Python Variables Scope

- No block-level scope.
- Initializing a variable in a `if`, `for` branch will make the variable available
  for the rest of the function.

## global and nonlocal
### `global`
Used to say that an identifier name used in the current code block should be interpreted
as global.
It would be impossible to assign a global variable without `global`
E.g.:
```python
a = 1
def foo():
    global a
    a += 1

foo()
print(a)
```

### `nonlocal`
Used to say that an identifier names used in the current code block should be interpreted
as the one in the nearest enclosing scope, i.e. non local and non global.
E.g.:
```python
def foo():
    a = 1
    def bar():
        nonlocal a
        a += 1
    bar()

foo()
```
