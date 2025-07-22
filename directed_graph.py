from collections import deque


class Vertex:
    # Represents a vertex in the graph, accepts a value and a list of neighbors (values).
    def __init__(self, value, neighbors=None):
        self.value = value
        self.neighbors = set(neighbors) if neighbors else set()
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
        self.dfs_cycle = False
        self.updated_dfs = False
        self.updated_bfs = False
        self.source = None

    def __repr__(self):
        edge_list = [(u, v) for u in self.vertices
                     for v in self.vertices[u].neighbors]
        return f"Graph(vertices={list(self.vertices)}, edges={edge_list})"

    # Returns the vertex with the given value if it exists.
    def get(self, value):
        return self.vertices[value]

    # Adds a vertex to the graph if it does not already exists (value based).
    def add_vertex(self, value):
        if value not in self.vertices:
            self.reset(False)

            self.vertices[value] = Vertex(value)

    # Removes a vertex from the graph if it exists (value based).
    def remove_vertex(self, value):
        if value in self.vertices:
            self.reset(True)

            # Remove the vertex from all neighbors' lists
            for vertex in self.vertices.values():
                vertex.neighbors.discard(value)

            # Remove the vertex itself
            self.vertices.pop(value)

    # Checks if the graph has a cycle using DFS.
    def has_cycle(self):
        if not self.updated_dfs:
            self.dfs()

        return self.dfs_cycle

    # Connects two vertices in a *directed* graph (value based).
    def connect(self, source, destination):
        if source != destination:
            # add vertices if they do not exist and reset the graph if necessary
            self.add_vertex(source)
            self.add_vertex(destination)

            self.vertices[source].neighbors.add(destination)

    # Disconnects two vertices in a *directed* graph (value based).
    def disconnect(self, source, destination):
        if source != destination and source in self.vertices and destination in self.vertices:
            self.reset(False)

            self.vertices[source].neighbors.discard(destination)

    # **helper** Paints a vertex with a specific color.
    def paint(self, value, color):
        if value in self.vertices and color in ['white', 'gray', 'black']:
            self.vertices[value].color = color

    # Returns the neighbors of a vertex (values).
    def get_neighbors(self, value):
        if value in self.vertices:
            return set(self.vertices[value].neighbors)

        else:
            return set()

    # Resets the properties of all vertices in the graph.
    def reset(self, hard_reset=False):
        self.dfs_cycle = False
        self.updated_dfs = False
        self.updated_bfs = False
        self.source = None

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
        def dfs_rec(vertice):
            nonlocal time

            self.get(vertice).color = 'gray'
            time += 1
            self.get(vertice).d = time

            for neighbor in self.get(vertice).neighbors:
                if self.get(neighbor).color == 'white':
                    dfs_rec(neighbor)

                if self.get(neighbor).color == 'gray':
                    self.dfs_cycle = True

            self.get(vertice).color = 'black'
            time += 1
            self.get(vertice).f = time

        # Start DFS from each unvisited vertex
        for vertex in self.vertices:
            if self.get(vertex).color == 'white':
                dfs_rec(vertex)

        self.updated_dfs = True
        self.updated_bfs = False

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
            for neighbor in self.get(vertex).neighbors:
                if self.get(neighbor).color == 'white':

                    q.append(neighbor)
                    self.get(neighbor).color = 'gray'
                    self.get(neighbor).d = self.get(vertex).d + 1
                    self.get(neighbor).parent = vertex

            self.get(vertex).color = 'black'

        self.updated_bfs = True
        self.updated_dfs = False

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
        if self.has_cycle():
            return None

        return [vertex.value for vertex in sorted([vertex for vertex in self.vertices.values()], key = lambda vertex : vertex.f, reverse = True)]
        
