# I/O redirection

See https://www.tldp.org/LDP/abs/html/io-redirection.html

```
  1>filename
      # Redirect stdout to file "filename."
   1>>filename
      # Redirect and append stdout to file "filename."
   2>filename
      # Redirect stderr to file "filename."
   2>>filename
      # Redirect and append stderr to file "filename."
   &>filename
      # Redirect both stdout and stderr to file "filename."
      # This operator is now functional, as of Bash 4, final release.

   M>N
     # "M" is a file descriptor, which defaults to 1, if not explicitly set.
     # "N" is a filename.
     # File descriptor "M" is redirect to file "N."
   M>&N
     # "M" is a file descriptor, which defaults to 1, if not set.
     # "N" is another file descriptor.
```

```
  2>&1
      # Redirects stderr to stdout.
      # Error messages get sent to same place as standard output.
        >>filename 2>&1
            bad_command >>filename 2>&1
            # Appends both stdout and stderr to the file "filename" ...
        2>&1 | [command(s)]
            bad_command 2>&1 | awk '{print $5}'   # found
            # Sends stderr through a pipe.
            # |& was added to Bash 4 as an abbreviation for 2>&1 |.

   i>&j
      # Redirects file descriptor i to j.
      # All output of file pointed to by i gets sent to file pointed to by j.

   >&j
      # Redirects, by default, file descriptor 1 (stdout) to j.
      # All stdout gets sent to file pointed to by j.
```

### Opening File Descriptors

FDs available are from 3 to `ulimit -n`: `exec FD-NUMBER<> /tmp/foobar`
(ofc this will not work in interactive bash)
```
$ exec 3<> /tmp/foobar
```

Auto allocation:
```
$ exec {newFd}<>/tmp/foobar
$ echo $newFd
...
```

### Closing File Descriptors
```
n<&-
Close input file descriptor n.
0<&-, <&-
Close stdin.
n>&-
Close output file descriptor n.
1>&-, >&-
Close stdout.
Child processes inherit open file descriptors. This is why pipes work. To prevent an fd from being inherited, close it.
```
