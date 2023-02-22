# Python Misc

## repr() vs str()
`str()`:
- goal: user friendly & readability
- informal string representation of an object

`repr()`:
- goal debugging, development, & unambiguity
- official string representation of an object

Both uses builtins `__str__` or `__repr__` to display the object.

## which command
Handy `which` implementations:
- `shutil.which()`
- `plumbum.local.which()`

## Pass additional pytest options

- Via the `PYTEST_ADDOPTS` env var.

- the `addopts` field in `pytest.ini`.

## Graph an histogram from values:

```python
import matplotlib.pyplot as plt

x = [1,2,3,4]

plt.hist(x, bins=24)
plt.show()
```

## Make a graph from edges

```python
import matplotlib.pyplot as plt
import networkx as nx

edges = [
(1,2),
(3,4),
(1,4),
]

G=nx.Graph()
G.add_edges_from(edges)

pos = nx.spring_layout(G, scale=8)
nx.draw(G, pos, with_labels=True, font_size=5)

plt.show()
```
