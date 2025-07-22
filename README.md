# Directed Graph

Python implementation of a mutable directed graph featuring DFS/BFS traversal, cycle detection, shortest path lookup, and topological sort.

---

## Vertex Class

Each `Vertex` instance represents one node in the graph.

### Vertex Fields

| Field     | Type          | Description                                                         |
|-----------|---------------|---------------------------------------------------------------------|
| `value`   | `Any`         | User supplied identifier for the vertex (must be hashable).         |
| `neighbors` | `set[Any]`  | Set of **outgoing** neighbor values (`value`s of adjacent vertices).|
| `color`   | `str`         | Traversal mark: `'white'` (unvisited), `'gray'` (in progress), `'black'` (finished). |
| `d`       | `int` | Discovery time in DFS, or distance from BFS source; `∞` by default. |
| `f`       | `int` | Finish time in DFS; `∞` by default.                                 |
| `parent`  | `Any`  | Predecessor value recorded by DFS/BFS; `None` if root or unreachable.|

---

## Graph Class

- **Constructor**  
  `Graph(vertices: Iterable[Any])`  
  Create an empty graph, or preload it with any hashable vertex values.

## Graph Fields

| Field | Type | Description |
|-------|------|-------------|
| `vertices`   | `dict[Any, Vertex]` | Mapping from **vertex value** → **Vertex object**. Stores the entire adjacency structure. |
| `dfs_cycle`  | `bool` | Set to `True` by `dfs()` if a back edge is encountered (i.e., the graph is cyclic). |
| `updated_dfs`| `bool` | `True` when the DFS metadata (`d`, `f`, `color`, `parent`, `dfs_cycle`) is up to date. Automatically cleared by any structural change. |
| `updated_bfs`| `bool` | `True` when the BFS metadata (`d`, `parent`) for the last `source` vertex is valid. Automatically cleared by any structural change. |
| `source`     | `Any` | The vertex value used as the root in the most recent `bfs()` call; `None` if no BFS has been run or the structure has changed since. |

## Functions 

- **Add Vertex**  
  `self.add_vertex(value)`
  Insert a new vertex if it does not already exist.

- **Remove Vertex**  
  `self.remove_vertex(value)`
  Delete a vertex and every incident edge.

- **Add Edge**  
  `self.connect(src, dst)`
  Add a directed edge src → dst; creates endpoints if needed. Self loops are ignored.

- **Remove Edge**  
  `self.disconnect(src, dst)`
  Remove the directed edge src → dst if present.

- **Get Vertex**  
  `self.get(value)`
  Return the Vertex object for value; raises KeyError if absent.

- **Neighbors**  
  `self.get_neighbors(value)`
  Return a copy of the neighbor set of `value` (or an empty set if the vertex is missing).

- **Cycle Detection**  
  `self.has_cycle()`
  Return True if the graph contains a directed cycle.

- **Depth First Search**  
  `self.dfs()`
  Label every vertex with discovery time d, finish time f, color, and parent; updates the cycle flag.

- **Breadth‑First Search**  
  `self.bfs(source)`
  Level order traversal from source; records distance d and parent for each reachable vertex.

- **Shortest Path**  
  `self.path(source, target)`  
  Return the shortest unweighted path source → … → target; returns an empty list if unreachable.

- **Topological Sort**  
  `self.topological_sort()`  
  Return a list of vertex values in topological order if the graph is acyclic; otherwise None.

- **(Debug) Reset Flags / State**  
  `self.reset(hard_reset: bool = False)`  
  Internal helper that invalidates DFS/BFS metadata after structural edits.  
  If `hard_reset=True`, it also clears every vertex’s traversal fields (`color`, `d`, `f`, `parent`).

- **(Debug) Paint**  
  `self.paint(value, color)`  
  Manually set the traversal color of a vertex ('white', 'gray', or 'black') for debugging.
