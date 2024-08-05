# C++

## Converting a C-string to int and check for errors

### Using stringstream

Note that `stringstream` is done to handle sequences of values.
So, when there's only a value to parse, we expect to parse it fully till EOF.

```
#include <sstream>

using namespace std;
bool convert(int* number, const char* cstr)
{
    stringstream ss(cstr);

    ss >> *number;

    //
    // fail is set if the string does not start with a number
    // eof is set only if we parse the full string till \0
    //
    if (ss.fail() || !ss.eof()) {
        cout << "CONVERSION FAILED" << endl;
        return false;
    }

    return true;
}
```

If needing to parse multiple value, then we can use `ss.peek() != ' '` to detect
error a check.

### override

Used to say that a derived class is overriding a virtual function of a base class.
`override` allows the compiler to check you are not doing mistakes e.g. not really
overriding a function, but e.g. overloading or defining a different one.

### virtual

Used  to say "may be redefined later in a derived  class". Pure virtual `= 0` means
the derived class _must_ define it (it makes the class an "abstract class").

>
> NOTE:
>
> - **There is no such thing as virtual constructor**. And note that
>   constructors are not inherited.
> - You can have **virtual destructors**.
> - You can have **pure virtual destructors**, but their body must _also_ be defined.
>   The purpose of them is to disallow to instantiate an object from that class.
>

### Virtual destructor

Making the base class destructor virtual guarantees that _also_ the derived class
destructor is properly called. The destructor are called from the deepest inheritance
level up to the base class.
Making a destructor virtual guarantees that all destructors are called.

## string_view

Lightweight non-owning read-only view into a subsequence of a string.

Instead of creating a full string with storage, it's just a string-like object
with a reference and a size to some memory where the string is stored.

Handy e.g. to:

- allow string-like `==` comparisons without creating a string out of a `const char*`:

```cpp
const char* foo = get_foo();
if (std::string_view{foo} == "1234") {
    ...
}
```

Create a `std::string`-like object out of a string literal, without the object
being created by copying the data from the string literal into the object.

```cpp
std::string_view good{"a string literal"};
```

## std::string operator s

It mainly allows to create a string out of a string literal that includes `\0`.
E.g. in the example below, without `s`, `str` would only include the characters
"foo".

```cpp
std::string str = "foo\0bar"s;
```

Or to get a substring out of a string:

## Types of inheritance

Variables:

- public: accessible everywhere
- protected: accessible only by derived classes
- private: accessible only by inside the class

Inheritance:

```
class A
{
    public:
       int x;
    protected:
       int y;
    private:
       int z;
};

class B : public A
{
    // Effect of using public inheritance:
    // x stays public
    // y stays protected
    // z is not accessible in this class
};

class C : protected A
{
    // Effect of using protected inheritance:
    // x becomes protected
    // y stays protected
    // z is not accessible in this class
};

class D : private A    // 'private' is default for classes
{
    // Effect of using private inheritance:
    // x becomes private
    // y becomes private
    // z is not accessible in this class
};
```

## Smart Pointers

### Shared Pointer

Shared pointer for a dynamically allocated uint8_t buffer.

```
std::shared_ptr<uint8_t> bufferPtr {new uint8_t[size]}, std::default_delete<uint8_t[]>()};
```

### Unique Pointer

Unique pointer for a dynamically allocated uint8_t buffer.

```cpp
std::unique_ptr<uint8_t []> bufferPtr {new uint8_t[size]};
//
//...
//
std::unique_ptr<uint8_t[]> anotherPtr = std::move(bufferPtr);
```
