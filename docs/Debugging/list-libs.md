# List of library dependencies of an executable

```
$ ldd [-v] <path_to_tool>
```

Or:
```
$ readelf -d <path_to_tool>
```

### List symbols used from specific libraries
```
$ readelf -a <executable>
```

(E.g. symbols used from GLIBC):
```
$ readelf -a <executable> | grep GLIBC*
```
