# Mixed Graph

Python implementation of a **mutable graph** that can hold directed and undirected edges. It supports DFS/BFS traversal, cycle detection, shortest‑path reconstruction, and topological sort (when the graph forms a DAG).

---

## Vertex Class

Each `Vertex` instance represents a single node.

### Vertex Fields

| Field       | Type             | Description                                                                                                            |
| ----------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `value`     | `Any`            | User‑supplied identifier (must be hashable).                                                                           |
| `neighbors` | `dict[Any, str]` | Mapping **neighbor value → edge kind**, where edge kind is `'directed'` (this → neighbor) or `'undirected'` (two‑way). |
| `color`     | `str`            | Traversal mark: `'white'` (unvisited), `'gray'` (in progress), `'black'` (finished).                                   |
| `d`         | `int`            | Discovery time in DFS, or distance from BFS source; `∞` by default.                                                    |
| `f`         | `int`            | Finish time in DFS; `∞` by default.                                                                                    |
| `parent`    | `Any`            | Predecessor recorded by traversal; `None` if root/unreachable.                                                         |

---

## Graph Class

```python
class Graph:
    def __init__(self, vertices = None):
        ...
```

Creates an empty graph or pre‑loads it with vertices. Edges can subsequently be added in *directed* or *undirected* form; the structure may therefore be **directed**, **undirected**, or **mixed**.

### Graph Fields

| Field              | Type                | Description                                                                          |
| ------------------ | ------------------- | ------------------------------------------------------------------------------------ |
| `vertices`         | `dict[Any, Vertex]` | Mapping *vertex value → Vertex*.                                                     |
| `directed_edges`   | `int`               | Count of directed edges (`u → v`).                                                   |
| `undirected_edges` | `int`               | Count of undirected edges (`u — v`).                                                 |
| `dfs_cycle`        | `bool`              | Set by `dfs()` when a back edge is detected (i.e., the current structure is cyclic). |
| `updated_dfs`      | `bool`              | `True` when DFS metadata is current.                                                 |
| `updated_bfs`      | `bool`              | `True` when BFS metadata for `source` is current.                                    |
| `source`           | `Any`               | Root used in the most recent `bfs()` (or `None` if none).                            |

---

## Public API

| Operation                 | Signature                                         | Effect                                                                                                             |
| ------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Add vertex**            | `add_vertex(value)`                               | Insert a vertex if absent.                                                                                         |
| **Remove vertex**         | `remove_vertex(value)`                            | Delete vertex and every incident edge.                                                                             |
| **Add *directed* edge**   | `connect_directed(u, v)`                          | Insert `u → v`; creates endpoints implicitly. Overwrites an existing undirected edge `u — v`.                      |
| **Add *undirected* edge** | `connect_undirected(u, v)`                        | Insert `u — v`; stored as two symmetric neighbor entries. Overwrites any existing directed edges between the pair. |
| **Remove edge**           | `disconnect(u, v)`                                | Delete edge(s) that originate at `u` (or both directions if the edge is undirected).                               |
| **Get vertex**            | `get(value)`                                      | Return the `Vertex` or `None`.                                                                                     |
| **Neighbors**             | `get_neighbors(value)`                            | Return a `set` with the neighbor values of `value`.                                                                |
| **Graph type**            | `type()`                                          | Return `'directed'`, `'undirected'`, or `'mixed'`.                                                                 |
| **Cycle detection**       | `has_cycle()`                                     | `True` iff the current graph contains a cycle (directed or undirected).                                            |
| **Depth‑First Search**    | `dfs()`                                           | Populate `d`, `f`, `color`, for every vertex.                                                             |
| **Breadth‑First Search**  | `bfs(source)`                                     | Level‑order traversal starting at `source`; records `d`, `parent`. `source` must exist in the graph.                                                |
| **Shortest path**         | `path(source, target)`                            | Reconstruct unweighted shortest path `source → … → target` (empty list if unreachable).                            |
| **Topological sort**      | `topological_sort()`                              | Return a topological ordering iff `type() == 'directed'` **and** `has_cycle()` is `False`; otherwise `None`.       |
| **Debug helpers**         | `reset(hard_reset=False)` / `paint(value, color)` | Clear traversal metadata / manually set a vertex color.                                                            |

---

## Edge Semantics

* **Directed** edge `u → v` is stored **once**: `u.neighbors[v] = 'directed'`.
* **Undirected** edge `u — v` is stored **twice**: both vertices list each other with edge kind `'undirected'`.

Mixing edge kinds is allowed; `type()` inspects the counts to classify the current structure.

---

## Complexity Notes

| Operation                                    | Time                                 | Space         |
| -------------------------------------------- | ------------------------------------ | --------------|
| `add_vertex`, `get`, `type`                  | **O(1)**                             | **O(1)**      |
| `get_neighbors`                              | **O(V)**                             | **O(V)**      |
| `remove_vertex`                              | **O(V)**                             | **O(1)**      |
| `connect_*`, `disconnect`                    | **O(1)**                             | **O(1)**      |
| `dfs`, `bfs`                                 | **O(V + E)**                         | **O(V)**      |
| `path`                                       | **O(V)** W.C                         | **O(V)**      |
| `topological_sort`, `has_cycle`              | **O(V + E)**                         | **O(V)**      |
