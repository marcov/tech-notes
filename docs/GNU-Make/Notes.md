# Notes on make

## Special variables

`@D`: the directory (`dirname`) of the target file.

## Some notes about `.PHONY` targets
From GNU Make manual:

A phony target should not be a prerequisite of a real target file; if it is,
its recipe will be run every time make goes to update that file. As long as a
phony target is never a prerequisite of a real target, the phony target recipe
will be executed only when the phony target is a specified goal (see Arguments
to Specify the Goals).

## How make timestamps work
>
> Does updating file contents in a directory always update the timestamp make looks at?
>

These are two different questions. One is about make behaviour, the other is about
directory timestamps behaviour.

In general, make only looks at mtime.

Hence when a directory mtime changes, if that directory is a prerequisite,
then make will rebuild the target

When a directory mtime changes?
Not as intuitive as it seems: https://www.baeldung.com/linux/directory-last-modified-time#conclusion

TLDR:

| Action                                                           | mtime changes  |
| ------                                                           | ------         |
|Renaming myDir                                                    | No             |
|Changing myDir‘s Permission                                       | No             |
|Changing the content of files under myDir                         | No             |
|Adding, removing, or renaming files or subdirectories under myDir | Yes            |

## Make variables

### Nomenclature

- When running `make MYVAR=value` then MYVAR is said to be set  with "a command
  argument". I.e., an argument that contains `=` specifies the value of a
  variable. By doing that, all ordinary assignments of the same variable in the
  `Makefile` being executed by `make` are ignored, i.e. the variable is
  _overridden_

- Normally make prints each line of the recipe before it is executed. This is
  called "recipe echoing", and it can be suppressed using `@`.

### Priority

TLDR - Priority of how a value is set:

1. (highest) value set in the makefile using the `override` keyword, e.g.
   `override VAR = value`.
2. value passed to make via a command argument e.g. `make VAR=value`
3. value set in the makefile, e.g. `VAR = value` or `VAR := value`
4. value set in an environment variable, e.g. `VAR=value make`
5. (lowest) value set in the makefile using conditional variable assignment,
   e.g. ` VAR ?= value`

From make man pages:
>
> Variables in make can come from the environment in which make is run. Every
> environment variable that make sees when it starts up is transformed into a
> make variable with the same name and value.
>
> However, an explicit assignment in the makefile, or with a command argument,
> overrides the environment.
>
> If the ‘-e’ flag is specified, then values from the environment override
> assignments in the makefile (but this is not recommended practice).
>

Given:
```makefile
VAREQ = equal
VARCOLON := colon
VARQUEST ?= question

all:
        @echo =  \'$(VAREQ)\'
        @echo := \'$(VARCOLON)\'
        @echo ?= \'$(VARQUEST)\'
```

```console
$ make
= 'equal'
:= 'colon'
?= 'question'
```

```console
$ make VAREQ="neweq" VARCOLON="newcolon" VARQUEST="newquest"
= 'neweq'
:= 'newcolon'
?= 'newquest'
```

```console
$ VAREQ="neweq" VARCOLON="newcolon" VARQUEST="newquest" make
= 'equal'
:= 'colon'
?= 'newquest'
```

```console
$ VAREQ="neweq" VARCOLON="newcolon" VARQUEST="newquest" make VAREQ="neweq2" VARCOLON="newcolon2" VARQUEST="newquest2"
= 'neweq2'
:= 'newcolon2'
?= 'newquest2'
```

```console
$ VAREQ="neweq" VARCOLON="newcolon" VARQUEST="newquest" make -e
= 'neweq'
:= 'newcolon'
?= 'newquest'
```

## Keep going

Continue as much as possible after an error.

```console
$ make --keep-going THE-TARGET
```

## Target and recipes using foreach

Using the following method, each command is a dedicate recipe line. If a
command fail, make will fail.

Instead, if you use bash `for ... in; do`, then a command failure does not
stop executing the next ones. And if the last command succeeds, then make exits
with 0.

Note: The empty line before `endef` is needed to expand each `recipe_line` into
a full recipe line.

```makefile
define recipe_line
	$(recipe_line_command) $(1) [other options ...]

endef

.PHONY: all
all:
	$(foreach arg,$(ALL_ARGUMENTS),$(call recipe_line,$(arg)))
```

```console
$ make ALL_ARGUMENTS="ciao belli" recipe_line_command="/usr/bin/echo"
/usr/bin/echo ciao [other options ...]
ciao [other options ...]
/usr/bin/echo belli [other options ...]
belli [other options ...]
```

## Spaces using in conditionals

Quoting: http://savannah.gnu.org/bugs/?59584

> For conditionals, preceding whitespace is preserved in the left-hand side of
> the match, while trailing space is ignored.  Bizarrely, for the right-hand
> side of the match leading whitespace is ignored while trailing whitespace is
> preserved.

> I always recommend to everyone that they remove all leading/trailing
> whitespace in all conditionals, as a simple to remember and always-correct
> rule.

Both evaluate to false:

```make
ifeq ( $(foo), $(foo))

# ...

ifeq ( $(foo),$(foo) )
```

Evaluate to true:

```make
ifeq ($(foo) , $(foo))
```
