# Implicit and Pattern Rules

Use the right implicit variable:

- Specify compiler flags in `CFLAGS` and `CXXFLAGS`
- Specify libraries to link against in `LDLIBS`
- Specify linker flags in `LDFLAGS`

NOTE: Using the right variable is important!
E.g., `LDLIBS` needs to appear after the source and object files when invoking
the compiler.

E.g.:

- foo: `CFLAGS = -Wall -g`
- bar: `LDLIBS = -lfoo`

Becomes:
```
$ cc -Wall -g  myapp.c -lfoo -o myapp
```

Instead:
`CFLAGS = -Wall -g -lfoo`
or
`CFLAGS = -Wall -g`
`LDFLAGS -lrt`
is an error, since it becomes:
```
$ cc -Wall -g -lfoo myapp.c -o myapp
/tmp/ccgbcs2S.o: In function `foo_caller':
myapp.c:10: undefined reference to `function_in_foo_lib'
```

## Pattern rules
Pattern rules are used to define a custom implicit rule.
`%` is the *stem* and is used in the recipe with `$*`

#### Format:
```
%.o: %.c
	echo "Building $*"
	# ...
```

### NOTE
Pattern rules *should* be used with targets that creates a file.
So using pattern rules with `.PHONY` is usually not the goal of such rules.
This is because when you define a `.PHONY` rule, Make search for an explicit rule.

## Static pattern rules
They are similar to simple pattern rules, but the difference is that you can limit
the scope of the pattern rule to a list of targets. Also, normal pattern rules
are order dependent, so you may not be sure what rule applies.

E.g.
```
TARGETS := foo.o bar.o

$(TARGETS): %.o: %.c
	$(ANOTHER_CC) -c $(ANOTHER_CFLAGS) $< -o $@
```

## Cancelling rules
**NOTE** Implicit rules with no recipe, it is a *cancelling rule*

So this will cancel any built-in implicit rule.

E.g: `%.o : %.c`
