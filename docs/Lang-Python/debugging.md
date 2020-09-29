# Python Debugging

### Debugger
You can have an on-the-fly breakpoint with:
```
import pdb; pdb.set_trace()
```
When running your app, it will break and give you a GDB-like CLI (print, next, step, ...)

### Print script name
```
print(__file__)
```
