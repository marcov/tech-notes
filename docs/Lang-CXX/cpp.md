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
> - **There is no such thing as virtual constructor**. And note that constructors are
>   not inherited.
> - You can have **virtual destructors**.
> - You can have **pure virtual destructors**, but their body must _also_ be defined.
>   The purpose of them is to disallow to instantiate an object from that class.
>

### Virtual destructor
Making the base class destructor virtual guarantees that _also_ the derived class
destructor is properly called. The destructor are called from the deepest inheritance
level up to the base class.
Making a destructor virtual guarantees that all destructors are called.

## Kind of inheritances
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
    // x is public
    // y is protected
    // z is not accessible from B
};

class C : protected A
{
    // x is protected
    // y is protected
    // z is not accessible from C
};

class D : private A    // 'private' is default for classes
{
    // x is private
    // y is private
    // z is not accessible from D
};
```
