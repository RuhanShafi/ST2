from graph import Graph

# =====================================================================
# Task 1 – Graph Basics: Add / Remove vertices & edges
# =====================================================================
print("=" * 60)
print("TASK 1: Graph Basics")
print("=" * 60)

# --- Undirected graph ---
print("\n-- Undirected Graph --")
g = Graph()
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_edge('A', 'B')
g.add_edge('B', 'C')
g.print_graph()

# --- Directed graph ---
print("\n-- Directed Graph --")
g = Graph(directed=True)
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_edge('A', 'B')
g.add_edge('B', 'C')
g.print_graph()

# --- Weighted directed graph ---
print("\n-- Weighted Directed Graph --")
g = Graph(weighted=True, directed=True)
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_edge('A', 'B', 15)
g.add_edge('B', 'C', 34)
g.print_graph()

# --- Removal tests ---
print("\n-- Removal Test --")
removal_test = Graph()
removal_test.add_vertex('A')
removal_test.add_vertex('B')
removal_test.add_vertex('C')
removal_test.add_edge('A', 'B')
removal_test.add_edge('B', 'C')
print("Initial graph:")
removal_test.print_graph()
removal_test.remove_edge('A', 'B')
print("After removing edge A-B:")
removal_test.print_graph()
removal_test.remove_vertex('C')
print("After removing vertex C:")
removal_test.print_graph()

# =====================================================================
# Task 2 – BFS Traversal
# =====================================================================
print("\n" + "=" * 60)
print("TASK 2: BFS Traversal")
print("=" * 60)

g = Graph()
for v in ['A', 'B', 'C', 'D']:
    g.add_vertex(v)
g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'D')
g.add_edge('C', 'D')
g.print_graph()

print("\nBFS starting from vertex 'A':")
visited_bfs = g.bfs('A')
print("Visited vertices in BFS order:", visited_bfs)

# =====================================================================
# Task 3 – DFS Traversal
# =====================================================================
print("\n" + "=" * 60)
print("TASK 3: DFS Traversal")
print("=" * 60)

print("\nDFS starting from vertex 'A':")
visited_dfs = g.dfs('A')
print("Visited vertices in DFS order:", visited_dfs)

# =====================================================================
# Task 4 – Cycle Detection in Undirected Graphs
# =====================================================================
print("\n" + "=" * 60)
print("TASK 4: Cycle Detection (Undirected)")
print("=" * 60)

# Graph WITH a cycle (triangle: A-B-C-A)
cycle_graph = Graph(directed=False)
for v in ['A', 'B', 'C']:
    cycle_graph.add_vertex(v)
cycle_graph.add_edge('A', 'B')
cycle_graph.add_edge('B', 'C')
cycle_graph.add_edge('C', 'A')   # closes the cycle
print("Does cycle_graph have a cycle?  ", cycle_graph.has_undirected_cycle())

# Graph WITHOUT a cycle (linear chain: X-Y-Z)
acyclic_graph = Graph(directed=False)
for v in ['X', 'Y', 'Z']:
    acyclic_graph.add_vertex(v)
acyclic_graph.add_edge('X', 'Y')
acyclic_graph.add_edge('Y', 'Z')
print("Does acyclic_graph have a cycle?", acyclic_graph.has_undirected_cycle())

# =====================================================================
# Task 5 – Weighted and Directed Graphs
# =====================================================================
print("\n" + "=" * 60)
print("TASK 5: Weighted Directed Graph")
print("=" * 60)

wg = Graph(directed=True, weighted=True)
for v in ['A', 'B', 'C']:
    wg.add_vertex(v)
wg.add_edge('A', 'B', weight=15)
wg.add_edge('B', 'C', weight=34)
wg.add_edge('A', 'C', weight=50)
print("Weighted Directed Graph:")
wg.print_graph()
print("\nWeights dict:", wg.weights)
