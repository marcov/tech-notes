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
