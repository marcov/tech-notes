# Python Data Structures

## Unpacking a list

Use `*`:
```
>>> l = list(range(5))
>>> a,b,*c=l
>>> print(a)
0
>>> print(b)
1
>>> print(c)
[2, 3, 4]
```

```
>>> l = ['foo', 'bar', *list(range(3)), 'fax']
>>> l
['foo', 'bar', 0, 1, 2, 'fax']
```

## Iterate over a sequence of tuples or list
a. Use `itertools.chain`:
```
a = list(range(5))
b = ('foo','bar','fax')
for v in itertools.chain(a,b):
    print(v)
```

a. Create a new list with `+`, converting the tuple to list:
```
a = list(range(5))
b = ('foo','bar','fax')
for v in a + list(b):
    print(v)
```

Either way it will print:
```
0
1
2
3
4
foo
bar
fax
```
