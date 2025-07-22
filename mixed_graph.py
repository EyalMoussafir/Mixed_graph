from collections import deque


class Vertex:
    # Represents a vertex in the graph, accepts a value and a list of *outgoing* (directed) neighbor values.
    def __init__(self, value, neighbors=None):
        self.value = value
        self.neighbors = {neighbor : 'directed' for neighbor in neighbors} if neighbors else dict()
        self.color = 'white'
        self.d = float('inf')
        self.f = float('inf')
        self.parent = None

    def __eq__(self, other):
        if not isinstance(other, Vertex):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"V({self.value!r})"


class Graph:
    # Represents a directed graph, accepts a list of vertices (values).
    def __init__(self, vertices=None):
        self.vertices = {val: Vertex(val) for val in vertices} if vertices else dict()

        # Indicates whether the graph has a cycle (using DFS).
        self.dfs_cycle = False

        # Indicates whether the DFS is up to date.
        self.updated_dfs = False

        # Indicates whether the BFS is up to date.
        self.updated_bfs = False
        self.source = None

        # Indicates the type of the graph (directed, undirected, mixed).
        self.undirected_edges = 0
        self.directed_edges = 0

    def __repr__(self):
        edge_list = [(u, v, self.vertices[u].neighbors[v]) for u in self.vertices for v in self.vertices[u].neighbors]
        return f"Graph(vertices={list(self.vertices)}, edges={edge_list})"

    # Returns the vertex with the given value if it exists.
    def get(self, value):
        return self.vertices.get(value)

    # Adds a vertex to the graph if it does not already exists (value based).
    def add_vertex(self, value):
        if value not in self.vertices:
            self.reset(False)

            self.vertices[value] = Vertex(value)

    # Removes a vertex from the graph if it exists (value based).
    def remove_vertex(self, value):
        if value in self.vertices:
            self.reset(True)

            # Remove all outgoing edges from the vertex
            for neighbor in list(self.get(value).neighbors.keys()):
                self.disconnect(value, neighbor)

            # Remove the vertex from all neighbors' lists
            for neighbor in self.vertices:
                self.disconnect(neighbor, value)

            # Remove the vertex itself
            self.vertices.pop(value)

    # Checks if the graph has a cycle using DFS.
    def has_cycle(self):
        if not self.updated_dfs:
            self.dfs()

        return self.dfs_cycle
    
    # Returns the type of the graph based on the edges.
    def type(self):
        if self.undirected_edges > 0 and self.directed_edges > 0:
            return 'mixed'
        elif self.undirected_edges > 0:
            return 'undirected'
        else:
            return 'directed'

    # Connects two vertices in a *directed* graph (value based).
    # If an undirected edge already exists between the vertices, it will be overwritten.
    def connect_directed(self, source, destination):
        if source != destination:
            # add vertices if they do not exist and reset the graph if necessary
            self.reset(False)

            self.add_vertex(source)
            self.add_vertex(destination)

            # If the connection already exists as undirected, remove it
            if self.vertices[source].neighbors.get(destination) == 'undirected':
                self.undirected_edges -= 1
                self.vertices[source].neighbors.pop(destination, None)
                self.vertices[destination].neighbors.pop(source, None)

            # If the directed edge does not already exist, add it
            if self.vertices[source].neighbors.get(destination) != 'directed':   
                self.directed_edges += 1
                self.vertices[source].neighbors[destination] = 'directed'

    # Connects two vertices in a *undirected* graph (value based).
    # If a directed edge already exists between the vertices, it will be overwritten.
    def connect_undirected(self, source, destination):
        if source != destination:
            # add vertices if they do not exist and reset the graph if necessary
            self.reset(False)

            self.add_vertex(source)
            self.add_vertex(destination)

            # If the connection already exists as directed, remove it
            if self.vertices[source].neighbors.get(destination) == 'directed':
                self.directed_edges -= 1
                self.vertices[source].neighbors.pop(destination, None)

            if self.vertices[destination].neighbors.get(source) == 'directed':
                self.directed_edges -= 1
                self.vertices[destination].neighbors.pop(source, None)

            # If the undirected edge does not already exist, add it
            if self.vertices[source].neighbors.get(destination) != 'undirected':
                self.undirected_edges += 1
                self.vertices[source].neighbors[destination] = 'undirected'
                self.vertices[destination].neighbors[source] = 'undirected'

    # Disconnects two vertices connection depending on the type of connection (value based).
    # If the edge between destination → source is undirected, both directions will be removed.
    # Otherwise, only the source → destination connection is removed (if it exists).
    def disconnect(self, source, destination):
        if source != destination and source in self.vertices and destination in self.vertices:
            self.reset(False)

            if self.vertices[destination].neighbors.get(source) == 'undirected':
                self.undirected_edges -= 1
                self.vertices[destination].neighbors.pop(source, None)
                self.vertices[source].neighbors.pop(destination, None)

            elif self.vertices[source].neighbors.get(destination) == 'directed':
                self.directed_edges -= 1
                self.vertices[source].neighbors.pop(destination, None)

    # Returns the neighbors of a vertex (values).
    def get_neighbors(self, value):
        if value in self.vertices:
            return set(self.vertices[value].neighbors.keys())

        else:
            return set()
        
    # **helper** Paints a vertex with a specific color.
    def paint(self, value, color):
        if value in self.vertices and color in ['white', 'gray', 'black']:
            self.vertices[value].color = color

    # **helper** Resets the properties of all vertices in the graph.
    def reset(self, hard_reset=False):
        self.updated_dfs = False
        self.updated_bfs = False
        self.dfs_cycle = False

        if hard_reset:
            for val in self.vertices.values():
                val.color = 'white'
                val.d = float('inf')
                val.f = float('inf')
                val.parent = None

    # Performs a depth-first search (DFS) on the graph.
    def dfs(self):
        self.reset(True)

        time = 0

        # Recursive DFS function
        def dfs_rec(vertex, parent=None):
            nonlocal time

            self.get(vertex).color = 'gray'
            time += 1
            self.get(vertex).d = time

            for neighbor, edge_type in self.get(vertex).neighbors.items():
                if self.get(neighbor).color == 'white':
                    dfs_rec(neighbor, vertex)

                if self.get(neighbor).color == 'gray' and edge_type == 'directed':
                    # Found a back edge in a directed graph
                    self.dfs_cycle = True

                elif self.get(neighbor).color == 'gray' and edge_type == 'undirected' and neighbor != parent:
                    # Found a back edge in an undirected graph
                    self.dfs_cycle = True

            self.get(vertex).color = 'black'
            time += 1
            self.get(vertex).f = time

        # Start DFS from each unvisited vertex
        for vertex in self.vertices:
            if self.get(vertex).color == 'white':
                dfs_rec(vertex)

        self.updated_dfs = True

    # Performs a breadth-first search (BFS) starting from the source vertex.
    def bfs(self, source):
        self.reset(True)
        self.source = source

        q = deque()

        q.append(source)
        self.get(source).color = 'gray'
        self.get(source).d = 0

        while q:
            vertex = q.popleft()
            for neighbor in self.get(vertex).neighbors.keys():
                if self.get(neighbor).color == 'white':

                    q.append(neighbor)
                    self.get(neighbor).color = 'gray'
                    self.get(neighbor).d = self.get(vertex).d + 1
                    self.get(neighbor).parent = vertex

            self.get(vertex).color = 'black'

        self.updated_bfs = True

    # Returns the shortest path from source to target using BFS.
    def path(self, source, target):
        if source not in self.vertices or target not in self.vertices:
            return []
        if not self.updated_bfs or self.source != source:
            self.bfs(source)
        if source == target:
            return [source]
        if self.get(target).parent is None:
            return []

        res = []
        tmp = target
        while tmp:
            res.append(tmp)
            tmp = self.get(tmp).parent
        res.reverse()
        return res
    
    # Returns a topological sort of the graph if it is a Directed Acyclic Graph (DAG).
    def topological_sort(self):
        # Check if the graph has a cycle and make sure DFS is valid
        if self.has_cycle() or self.type() != 'directed':
            return None

        return [vertex.value for vertex in sorted(self.vertices.values(), key = lambda vertex : vertex.f, reverse = True)]
        
