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
