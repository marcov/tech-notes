# C / C++

## Declaration vs Definition
- Declaration: specify the properties of an identifier.
  * only specifies the type of a variable, not its value.
  * only specifies the type signature of a function, not its body.

Examples of declarations that are NOT definitions, in C:
```
extern char example1;
extern int example2;
void example3(void);
```

- Definition:
  * assign a value to variables
  * supply the implementation body to a function

Examples of declarations that are definitions, again in C:
```
char example1; /* Outside of a function definition it will be initialized to zero.  */
int example2 = 5;
void example3(void) { /* definition between braces */ }
```

## volatile
Sum up from: https://lwn.net/Articles/233479/

The purpose of volatile is to force an implementation to **suppress optimizations**
that could otherwise occur. For example, for a machine with memory-mapped
input/output, a pointer to a device register might be declared as a pointer to
volatile, in order to prevent the compiler from removing apparently redundant
references through the pointer.

The point that Linus often makes with regard to volatile is that its purpose is
to suppress optimization, which is almost never what one really wants to do.
In the kernel, one must protect accesses to data against race conditions, which
is very much a different task.

Given:
```
    spin_lock(&the_lock);
    do_something_on(&shared_data);
    do_something_else_with(&shared_data);
    spin_unlock(&the_lock);
```
The spinlock primitives act as memory barriers - they are explicitly written to
do so - meaning that data accesses will not be optimized across them.

If shared_data were declared volatile, the locking would still be necessary.
But the compiler would also be prevented from optimizing access to shared within
the critical section, when we know that nobody else can be working with it.
While the lock is held, shared_data is not volatile.

> "Data isn't volatile - _accesses_ are volatile".

When dealing with shared data, proper locking makes volatile unnecessary - and potentially harmful.
The volatile storage class was originally meant for memory-mapped I/O registers.

## Syntactical elements definition
### Expression
An operator with its arguments, a function call, a constant, a variable name, etc...

### Primary expression
- Constants / literals
- Identifiers

### Expression statement
An expression followed by a semicolon. Most of the statements are expression statements.
```
a = 1;
```

### Statements
Fragments executed in sequence

- Declaration statement
- Expression statement
- Return statement
- ...

### Compound statement
Brace enclosed sequence of statements.
```
{ int a = 1; a = 2; }
```

### Statement expression
 * This evaluates into the last expression inside `({})`:
   ```
   int bar = ({ int foo = 2; ... ; foo; });
   // bar is 2
   ```

 * **PROBLEM**: it can shadow variables, making the code broken....
   ```
   const int b = 123;
   int a = 4;
   ({int a = (a); a > b ? a : b;});
   ```

More info: https://gcc.gnu.org/onlinedocs/gcc/Statement-Exprs.html#Statement-Exprs

### Array of characters initialization

>
> An array of character type may be initialized by a character string literal,
> optionally enclosed in braces. Successive characters of the character string
> literal (including the terminating null character if there is room or if the
> array is of unknown size) initialize the elements of the array.
>

So these are equivalent:
```
char foo[] = "ciao";

char foo[] = {"ciao"}; // Optionally enclosed in braces

char foo[] = {'c', 'i', 'a', 'o'};
```

`char *` variables, CANNOT be initialized with an array of characters:
```
// ERROR!
char* foo = {'c', 'i', 'a', 'o'};
```

### Comma AS operator
 * Separates expressions (NOT statements).

 * Evaluates the first operator, discards result; then evaluates the second operator
   and returns this value.

 * Does NOT need to be wrapped with parenthesis `()`. E.g. is a valid statement:
   ```
   a = 1, a+= 2;
   ```

 * Can have as many comma as needed. E.g. this is a valid statement:
   ```
   1,2,3,a = 4;
   ```

### Enumerations (C++)
#### Unscoped Enumerations
> NOTE: `[ : type ]` here means may or may not have inheritance from `: type` specified.

- Declared as: `enum Foobar [ : type ] { a = 0, b = 1, c = 2 };`
- Implicitly convertible to integral type: `int n = a;`

#### Scoped Enumerations
Declared as: `enum struct Foobar [ : type ] { a = 0, b = 1, c = 2 }; `, `enum class Foobar  [ : type ] { ... `
- NOT implicitly convertible to integral type: `int n = Foobar::a;` (can use static_cast<int> though)

### List Initializations (C++)
- Direct: `Type objectName {arg1, arg2, ...};`
- copy-list: `Type objectName = {arg1, arg2, ...};`

### Variadic macros
A macro declared to accept a variable number of arguments, like a function can do.
```
#define eprintf(...) fprintf (stderr, __VA_ARGS__)
```

### Data Types

- Scalar Types: _all of the values lie along a linear scale_
  * Arithmetic Types
    + Integral Types
      - Plain integers
      - Characters
      - (Boolean, but note that boolean is still an int for plain C)
    + Floating types
  * Pointers
  * Enumerated types

- Aggregate Types: _built by combining more scalar types_
  * Arrays
  * Structures
  * Unions

- `void`

### Trigraph sequences
Before any other processing takes place, each occurrence of one of the following
sequences of three characters (called trigraph sequences) is replaced with the
corresponding single character.
```
        ??=      #                       ??)      ]                       ??!     |
        ??(      [                       ??'      ^                       ??>     }
        ??/      \                       ??<      {                       ??-     ~
```

No other trigraph sequences exist. Each `?` that does not begin one of the
trigraphs listed above is not changed.

```
           ??=define arraycheck(a, b) a??(b??) ??!??! b??(a??)
```
becomes
```
           #define arraycheck(a, b) a[b] || b[a]
```
NOTE: with GCC, use the `-trigraphs` flag to enable trigraphs use.

### Pointer to member functions (C++)

A pointer to a member function can be used as a callback. You can pass it around
as a C function pointer.
To invoke the function, use the `.*` or `->*` operator:
- left side: the class object instance (or a pointer to it).
- right side: the pointer to the member fn.

E.g.:
```
struct C
{
    void f(int n) { std::cout << n << '\n'; }
};

int main()
{
    void (C::* p)(int) = &C::f; // pointer to member function f of class C
    C c;
    (c.*p)(1);                  // prints 1
    C* cp = &c;
    (cp->*p)(2);                // prints 2
}
```
