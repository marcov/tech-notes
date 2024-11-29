# awk

More info: [Idiomatic awk](https://backreference.org/2010/02/10/idiomatic-awk/index.html)

General form: `condition { actions }`.

`condition`: something that evaluates to true/false, e.g.:

- `1` (always true, always run the action).
- `/pattern/`
- `$0 ~ /pattern/`

`actions`: when not specified, default action is `print $0;`

## Print multiple lines on the same row:

```sh
echo "a\nb\nc" | awk '{printf("%s,",$0);}'
a,b,c,
```

## Change separator when printing fields

Use `OFS` + the "magic" `$1=$1` statement. The magic statement is used for
force re-computation of $0.

```sh
echo "a b c" | awk 'BEGIN {OFS=",";} {$1=$1} 1'
a,b,c
```

Or also:

```sh
echo "a b c" | awk -v OFS=',' '{$1=$1}1'
```

## Filter lines by regex

```awk
/foo.*bar/
```

## Filter lines by line number

```sh
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
