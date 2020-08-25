# Thread local storage

Allocate one instance of a variable per thread.
Can be applied to:
- A global variable
```
__thread int i;
```
- A static variable file-scoped OR function-scoped
```
static __thread char *p;
```
- A static data member of a class

CANNOT be applied to automatic variables (there's no point in doing it!)

