# Generate code coverage information

1. Build code with compile flags: `-fprofile-instr-generate`, `-fcoverage-mapping`

2. Link the code with flags: `-fprofile-instr-generate`

3. Run your executable (one or multiple times...)
   By default, the profile data will be written to a `default.profraw` file in
   the current directory.
   Override this with LLVM_PROFILE_FILE
   (e.g.: `LLVM_PROFILE_FILE="code-%p.profraw" ./executable`, `%p` is set to the process ID)

4. Generate profile data from one or multiple run of your program
```
$ llvm-profdata merge -output=code.profdata default.profraw
```

5. Use `llvm-cov` to generate a report from the profile data file:
```
$ llvm-cov report -instr-profile code.profdata ./path/to/executable ./path/to/source/code
```
Example output:

```
Filename                      Regions    Missed Regions     Cover   Functions  Missed Functions  Executed       Lines      Missed Lines     Cover
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
XXXXXXXXXX.cpp                     61                 6    90.16%           1                 0   100.00%         164                 6    96.34%
YYYY.cpp                          139                27    80.58%           3                 0   100.00%         231                37    83.98%
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
TOTAL                             200                33    83.50%           4                 0   100.00%         395                43    89.11%
```

More info: https://clang.llvm.org/docs/SourceBasedCodeCoverage.html#id2
