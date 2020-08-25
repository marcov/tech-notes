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

