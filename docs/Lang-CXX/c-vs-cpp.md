# C vs C++

## Common things

Order of evaluation of function arguments is unspecified!
This code is not guaranteed to print values in any order.

```cpp
int array[] = {1,2,3,4};
int* ptr = array;
//printf("%d %d %d %d\n", *ptr++, *ptr++, *ptr++, *ptr++);
```

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

```cpp
char myArray[5] = { [0] = 123, [1] = 456, [2] = 789 };

StructType myStruct = { .foo = 1, .bar = 2 };
```

Info: https://en.cppreference.com/w/cpp/language/aggregate_initialization#Designated_initializers

### Zero Initialization

**Empty initializer** list `{}` it's used for zero initialization of arrays.
It is valid in C++ but not in C until C23:

```cpp
int a[3] = {}; // valid C++ way to zero-out a block-scope array; valid in C since C23
int a[3] = {0}; // valid C and C++ way to zero-out a block-scope array
```

**NOTE** for C++ about structures and classes:

You cannot use `struct = {0}` to zero initialize all fields in a structure.
The effect is same as "aggregate-initialization". All these are equivalent:

```cpp
struct MyStruct foo = {};
```

```cpp
struct MyStruct foo{};
```

```cpp
struct MyStruct foo = MyStruct();
```

### Variable Length Arrays (VLAs) are NOT allowed in C++

```c
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
