# I/O redirection

See https://www.tldp.org/LDP/abs/html/io-redirection.html

```sh
  M > N
     # M is a file descriptor, which defaults to 1, if not explicitly set.
     # N is a FILENAME.
     # File descriptor M is redirect to file "N."

    > FILENAME
  1 > FILENAME
      # Redirect stdout to file FILENAME

    >> FILENAME
  1 >> FILENAME
      # Redirect and append stdout to file FILENAME

  2 > FILENAME
      # Redirect stderr to file FILENAME

  2 >> FILENAME
      # Redirect and append stderr to file FILENAME

  &> FILENAME
      # Redirect both stdout and stderr to file FILENAME
      # This operator is now functional, as of Bash 4, final release
```

```sh
  M > &N
     # M is a file descriptor, which defaults to 1, if not set.
     # N is another file descriptor.

  2 > &1
     # Redirects stderr to stdout.
     # Error messages get sent to same place as standard output.

  >> FILENAME 2>&1
     # Appends both stdout and stderr to the file FILENAME

  2 > &1 | [command(s)]
     # Sends stderr through a pipe.
     # |& was added to Bash 4 as an abbreviation for 2>&1 |.

  i > &j
     # Redirects file descriptor i to j.
     # All output of file pointed to by i gets sent to file pointed to by j.

  > &j
     # Redirects, by default, file descriptor 1 (stdout) to j.
     # All stdout gets sent to file pointed to by j.
```

### Opening File Descriptors

FDs available are from 3 to `ulimit -n`: `exec FD-NUMBER<> /tmp/foobar`
(ofc this will not work in interactive bash)

```sh
$ exec 3<> /tmp/foobar
```

Auto allocation:

```sh
$ exec {newFd}<>/tmp/foobar
$ echo $newFd
...
```

### Closing File Descriptors

```sh
N<&-
#Close input file descriptor N.

0<&-, <&-
#Close stdin.

N>&-
#Close output file descriptor N.

1>&-, >&-
#Close stdout.
#Child processes inherit open file descriptors. This is why pipes work. To prevent an fd from being inherited, close it.
```
