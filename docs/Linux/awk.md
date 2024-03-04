# awk

## Print multiple lines on the same row:

```awk
echo "a\nb\nc" | awk '{printf("%s,",$0);}'
a,b,c,
```

## Change separator when printing fields

Use `OFS` + the "magic" `$1=$1` statement:

```awk
echo "a b c" | awk 'BEGIN {OFS=",";} {$1=$1; print $0;}'
a,b,c
```

## Filter lines by regex

```awk
/foo.*bar/
```

## Filter lines by line number

```awk
awk 'NR <= 10'
```

## Print numbers with thousands separator

Use the printf `%\047d` format.

```console
$ echo 1234567 | awk '{printf("%\047d\n", $0);}'
1,234,567
```

## Escape single quote '

Use `'\''`.

```awk
# Replace ' with whitespace:
awk '{gsub(/'\''/, "", $0); print $0;}'
```
