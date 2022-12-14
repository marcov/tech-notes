# C / C++

## Declaration vs Definition

### Declaration

Specify the properties of an identifier:

  * only specifies the type of a variable, not its value.
  * only specifies the type signature of a function, not its body.

Examples of declarations (**NOT** definitions) in C:
```
extern char example1;
extern int example2;
void example3(void);
```

### Definition

  * assign a value to variables
  * supply the implementation body to a function

A definition is _always_ _also_ a declaration, but not vice versa.
Definitions are super-set of declarations.

Examples of definitions, again in C:
```
char example1; /* Outside of a function definition it will be initialized to zero.  */
int example2 = 5;
void example3(void) { /* definition between braces */ }
```

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

### Compound literals

Constructs an unnamed (temporary) object of specified type (which may be
struct, union, or even array type) in-place: `( type ) { initializer-list }`

```c
struct my_struct
{
    int a;
    char b;
    int c[12];
};

void fx(struct my_struct s)
{
    (void)s;
}

int main(void)
{
    fx((struct my_struct){1, 2, {1, 2, 3}});
    return 0;
}
```

Inline temporary array:

```c
static void print_array(const int* ptr);

print_array((const int []){1, 2, 3, 4});
print_array((const int [10]){1, 2,});
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
