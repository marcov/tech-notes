# awk

Merge lines:

```awk
awk '{printf("%s ", $0);}'
```

Change output separator: use `OFS` + the "magic" `$1=$1` statement:

```awk
BEGIN {OFS="S";} {$1=$1; print $0;}
```

Filter lines by regex:

```awk
/foo.*bar/
```

Filter lines by line number:

```awk
awk 'NR <= 10'
```

Print numbers with thousands separator using the printf `%\047d` format:

```console
$ echo 1234567 | awk '{printf("%\047d\n", $0);}'
1,234,567
```

Escape single quote `'` with `'\''`:

```awk
# Replace ' with whitespace:
awk '{gsub(/'\''/, "", $0); print $0;}'
```
