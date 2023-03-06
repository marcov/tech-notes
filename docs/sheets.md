# Google Sheets / Excel "advanced" uses

# Array

## Specify an array

As a single row:

```
{1, 2, 3, 4}
```

As a single column:

```
transpose({1, 2, 3, 4})
```

You can also turn a named range into an array:

This makes sheet expand the named range content into some other cells.

```
= {namedRange}
```

### Subarray

Subarray starting from an arbitrary offset. NOTE: Offset `-th` starts from 0!

```
offset(range, row-0th, col-0th, [rows-numof], [cols-numof])
```

Subarray starting from ofset 0

```
array_constrain(array, rows-numof, cols-numof)}
```

Get a single element. NOTE: index `-th` starts from 1!

```
index(array, [row-th], [col-th])
```

### Get index of a value

NOTE: returned value starts from 1!

```
match("key", array, 0)
# 0 = exact search -^
```

### Index one array, get the value from another array

Combine `index` and `match`

Search for a key in one array, get index of the key, and use that index to index a second array:

```
=index(array_2,,match("key", array_1, 0))
```

E.g., this returns 30 (when using named ranges for arrays this starts to make more sense):

```
=index({10, 20, 30, 40},,match("c", {"a", "b", "c", "d"}, 0))
```

## arrayformula

`arrayformula` allows to use arrays and named ranges in formulas.

E.g. you can do a multiplication with:

```
= arrayformula(namedRange * A1:A10)
```
