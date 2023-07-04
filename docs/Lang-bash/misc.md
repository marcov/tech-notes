# Misc

## Re-exec a shell on the fly
E.g., to apply new shell dotfiles config on-the-fly:
```
$ exec -l $SHELL
```
`-l`: place a `-` at the beginning of the 1st argument passed
Used for a login shell:
>
> A login shell is one whose first character of argument zero is a -,
> or one started with the --login option.
>

## Turn any command into a file (descriptor)

Use `<(cmd)`:

```
$ vi <(ls -ls /)

$ diff -Naur <(ls -ls /) <(ls -ls /mnt)
```

## `XDG*` variables
TL;DR: variables sets when the user logs in! So don't use them in non-login scripts
(e.g. cron jobs) with out a fallback: `${XDG_RUNTIME_DIR:-/tmp}`

### `XDG_RUNTIME_DIR`
It is an environment variable that is set automatically when you log in.

It tells any program you run where to find a user-specific directory in which it
can store small temporary files.

Note that `XDG_RUNTIME_DIR` is set by `pam_systemd(8)`, so it is not actually
related to X (running programs graphically), which is the problem you seem to
be having.

### Setting a script arguments with set `set`
Use `set -- list of args`
```
$ set -- foo bar fax
$ echo $@
foo bar fax
```

## Read all words from stdin (pipe)

> Note: xargs cannot be used here, since we need to invoke the command once for each
> word
```
docker images | grep IMGPATTERN | awk '{print $1":"$2}' | while read -r img; do docker push $img; done
```

## Read all lines in a file

```
$ while read -r line; do COMMAND; done < input.file
```

## cat as a shell built-in
```
function cat {
  # if there's only one arg, not starting with a `-`
  if [ $# -eq 1 -a "${1:0:1}" != "-" ]
  then
    # open the input file with fd=3
    exec 3< "${1:-/dev/stdin}"
    while read -r -u3 line
    do
      echo -E ''"${line}";
    done
    echo -nE ''"${line}";
    exec 3<&-
  else
     /bin/cat "$@"
  fi
}
```

## wait -n

The -n option tells bash to only wait for **one** PID or jobspec from the
provided arguments - whatever terminates first.

E.g.:
```
# Will only wait for the first PID that terminates among {1,2,3,4}.
$ wait -n 1 2 3 4

# Will wait for all PIDs
$ wait 1 2 3 4
```
