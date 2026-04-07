from collections import deque

class Graph:
    def __init__(self, directed=False, weighted=False):
        self.graph = {}       # adjacency list
        self.weights = {}
        self.directed = directed
        self.weighted = weighted

    # ------------------------------------------------------------------ #
    # Vertex / Edge management
    # ------------------------------------------------------------------ #

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2, weight=0):
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].append(vertex2)
            if self.weighted:
                self.weights[(vertex1, vertex2)] = weight
            if not self.directed:
                self.graph[vertex2].append(vertex1)
                if self.weighted:
                    self.weights[(vertex2, vertex1)] = weight
        else:
            print("One or both vertices not found in graph.")

    def remove_vertex(self, vertex):
        if vertex in self.graph:
            del self.graph[vertex]
            # Remove all edges pointing to this vertex
            for v in self.graph:
                if vertex in self.graph[v]:
                    self.graph[v].remove(vertex)
            # Remove weights involving this vertex
            keys_to_del = [k for k in self.weights if vertex in k]
            for k in keys_to_del:
                del self.weights[k]
        else:
            print(f"Vertex '{vertex}' not found.")

    def remove_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph[vertex1]:
            self.graph[vertex1].remove(vertex2)
            if self.weighted and (vertex1, vertex2) in self.weights:
                del self.weights[(vertex1, vertex2)]
            if not self.directed:
                self.graph[vertex2].remove(vertex1)
                if self.weighted and (vertex2, vertex1) in self.weights:
                    del self.weights[(vertex2, vertex1)]
        else:
            print("Edge not found.")

    def print_graph(self):
        for vertex in self.graph:
            if self.weighted:
                edges = [(nbr, self.weights.get((vertex, nbr), '?'))
                         for nbr in self.graph[vertex]]
                print(f"{vertex}: {edges}")
            else:
                print(f"{vertex}: {self.graph[vertex]}")

    # ------------------------------------------------------------------ #
    # Task 2 – BFS
    # ------------------------------------------------------------------ #

    def bfs(self, start):
        if start not in self.graph:
            print(f"Start vertex '{start}' not in graph.")
            return []
        visited = []
        queue = deque([start])
        seen = {start}
        while queue:
            vertex = queue.popleft()
            visited.append(vertex)
            for nbr in self.graph[vertex]:
                if nbr not in seen:
                    seen.add(nbr)
                    queue.append(nbr)
        return visited

    # ------------------------------------------------------------------ #
    # Task 3 – DFS
    # ------------------------------------------------------------------ #

    def dfs(self, start):
        if start not in self.graph:
            print(f"Start vertex '{start}' not in graph.")
            return []
        visited = []
        stack = [start]
        seen = set()
        while stack:
            vertex = stack.pop()
            if vertex not in seen:
                seen.add(vertex)
                visited.append(vertex)
                for nbr in reversed(self.graph[vertex]):
                    if nbr not in seen:
                        stack.append(nbr)
        return visited

    # ------------------------------------------------------------------ #
    # Task 4 – Cycle detection (undirected)
    # ------------------------------------------------------------------ #

    def has_undirected_cycle(self):
        visited = set()

        def dfs_cycle(current, parent):
            visited.add(current)
            for nbr in self.graph[current]:
                if nbr not in visited:
                    if dfs_cycle(nbr, current):
                        return True
                elif nbr != parent:
                    return True
            return False

        for vertex in self.graph:
            if vertex not in visited:
                if dfs_cycle(vertex, None):
                    return True
        return False

    # ------------------------------------------------------------------ #
    # Bonus – Cycle detection (directed)  – used in Task 8
    # ------------------------------------------------------------------ #

    def has_directed_cycle(self):
        visited = set()
        rec_stack = set()

        def dfs(v):
            visited.add(v)
            rec_stack.add(v)
            for nbr in self.graph[v]:
                if nbr not in visited:
                    if dfs(nbr):
                        return True
                elif nbr in rec_stack:
                    return True
            rec_stack.remove(v)
            return False

        for vertex in self.graph:
            if vertex not in visited:
                if dfs(vertex):
                    return True
        return False
