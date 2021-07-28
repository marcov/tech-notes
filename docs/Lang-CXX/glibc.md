# glibc

## Numeric conversion functions
`atof, atoi, atol, and atoll` are **UNSAFE**:
_If the value of the result cannot be represented, the behavior is undefined_

## Path resolution vs. path canonicalization

What's the different b/w `canonicalize_file_name()` ( `realpath()`) and `readlink()`?

- `readlink()` need as input a symbolic link, and jut read its value. Period.

- `canonicalize_file_name()` / `realpath()`:
  * always returns an absolute file path.
  * recursively resolves all symbolic link.
  * does not accept circular loops in symbolic link.
  * does not accept symbolic link pointing to non-existing files.
  * to succeed, it requires the resolved path to exist.
