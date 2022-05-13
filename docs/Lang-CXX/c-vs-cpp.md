# C vs C++

## Differences between modern-ish C and plain C++ standards

### Designated initializers for arrays and structures.

> **Note**:
> - designated initializers is a form of aggregate initialization,
>   i.e. initializers of an aggregate type using `{ }`
>
> - Added to C++20, but this is still invalid:
>    * Out of order (`[1] = 123, [0] = 456`)
>    * Nested (`.a.b = ...`)
>    * mixed (designated and not)

```
char myArray[5] = { [0] = 123, [1] = 456, [2] = 789 };

StructType myStruct = { .foo = 1, .bar = 2 };
```

Info: https://en.cppreference.com/w/cpp/language/aggregate_initialization#Designated_initializers

### Zero Initialization

Empy initializer list `{}` it's used for zero initialization.
It is valid in C++ but not in C until C99:
```
//
// NOTE:
// - cannot assign to a struct = {0} to make it zero intialized.
// - the effect is same as: A a{}; or A a = {};
//
struct MyStruct foo = {};
// or equivalent
struct MyStruct foo{};
// or equivalent
struct MyStruct foo = MyStruct();

// For arrays, "= {}" is equivalent to "= {0}"
char myArray[1234] = {};
```

### Variable Length Arrays (VLAs) are NOT allowed in C++
```
void foobar(unsigned int n)
{
    unsigned int foo[n];
    ...
}
```

### String literals must be immutable in C++ (`const`)
```
char* myStr = "foobar"; // valid in C; error in C++

const char* myStr = "foobar"; // valid in C and C++
```

(Better) idiomatic C++:
```
auto myStr = "foobar";
```

Make the pointer itself immutable:
```
constexpr auto Foo = "bar";
// OR
constexpr const char* Foo = "bar";
```

### Arithmetic on void pointers
Arithmetic on void pointers is allowed in the _GNU extension_ to C, but not in C++
(even in GNU extensions).

```
void* foo;

foo += 2;
```

### const qualifier
- C++: `const` used on a non-local, non-volatile, non-inline variable gives it
  internal linkage, unless `extern` is explicitly specified.
- C: file-scope `const` variables have external linkage by default.

### Overloading and Name Mangling
- C++ supports functions overload, using name mangling.
- C does not support name mangling, so it does not use overload.

You can tell the C++ compiler not to mangle specific part of the code, so that
it will emit object codes with their name un-mangled, using `extern "C"`.
This way, you will be able to link this object with C only objects:

Compile with `-c`:
```
// exit reference is un-mangled:
extern "C"
void exit (int __status);
int main(void)
{
    exit(0);
    return 0;
}
```

Without `extern "C"`:
```
$ nm a.out
                 U _GLOBAL_OFFSET_TABLE_
0000000000000000 T main
                 U _Z4exiti
```

With `extern "C"`:
```
$ nm a.out
                 U exit
                 U _GLOBAL_OFFSET_TABLE_
0000000000000000 T main

```
