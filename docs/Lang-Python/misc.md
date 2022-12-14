# Python Misc

## repr() vs str()
`str()`:
- goal: user friendly & readability
- informal string representation of an object

`repr()`:
- goal debugging, development, & unambiguity
- official string representation of an object

Both uses builtins `__str__` or `__repr__` to display the object.

## which command
Handy `which` implementations:
- `shutil.which()`
- `plumbum.local.which()`

## Pass additional pytest options

- Via the `PYTEST_ADDOPTS` env var.

- the `addopts` field in `pytest.ini`.
