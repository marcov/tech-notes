# Bash Shortcuts

## Prompt Editing

>
>**NOTE**: these are effectively readline shortcuts.
>

Arrows alternative:

`C-b`: backward one char (like <-)
`C-n`: down one line (like ^)
`C-p`: up one line (like v)
`C-f`: forward one char (like ->)

`C-a`: begin of line

`C-e`: end of line

`A-b`: backward one word
`A-f`: forward one word

`C-h`: delete previous character
`C-d`: delete next character

`C-w`: delete previous word
`A-d`: delete next word

`C-k`: delete from cursor position to EOL
`C-u`: delete from cursor position to Begin Of Line (in bash, zsh needs remapping)

`C-l`: clears screen

### CTRL-v
Press `C-v` followed by any character to get the `C-*` combination for
that specific character.

E.g.: `C-v` followed by <Enter> gives `^M`, so Enter can be replaced by `C-m`

## Signaling

See the current key mappings with:
```
$ stty -a
```

`C-c`: SIGINT: interrupt the process

`C-z`: SIGSTOP: stop a process for later resumption

`C-\`: SIGQUIT: quit and perform a coredump

These key combinations are handled by the terminal device driver.
They can be changed in terminal settings using `tcsetattr(3)`:
```
c_lflag flag constants:
  ISIG   When any of the characters INTR, QUIT, SUSP, or DSUSP are received,
         generate the corresponding signal.

  VSUSP  (032,  SUB,  Ctrl-Z)  Suspend character (SUSP).  Send SIGTSTP signal.
         Recognized when ISIG is set, and then not passed as input.
```

In a shell, use:

- bash: `bind`
- zsh: `bindkey`

### More info

- https://readline.kablamo.org/emacs.html

- https://effective-shell.com/docs/section1/1-navigating-the-command-line/images/command-line.png

### Repeating commands from history

```
$ echo foobar
foobar

# Repeat last command
$ !
foobar

# Repeat last command starting with e
$ !e
foobar

# Repeat last command starting with e
$ !e
foobar

# Repeat last command having the foobar word
$ !?foobar
```

Substitution:

```
# Substitute "foo" with "baz" in last command
$ ^foo^baz
bazbar

# Same as before:
$ !!:s^foo^baz

# Substitute in last matching command start:
$ !e:s^foo^baz
```
