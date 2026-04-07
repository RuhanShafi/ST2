from graph import Graph
import tkinter as tk
import math
import time
import threading

USE_DIRECTED = True   # change to True to test directed cycle detection


class GraphVisualizer(tk.Tk):

    def __init__(self, graph):
        super().__init__()
        self.title("Graph Visualizer – Extended (Task 8)")
        self.geometry('680x700')
        self.graph = graph

        self.canvas = tk.Canvas(self, width=600, height=520, bg='white')
        self.canvas.pack(pady=10)

        self.vertex_positions = {}
        self.node_radius = 22
        self.spacing = 180
        self.center = (300, 260)

        self.vertex_circles = {}   # vertex -> canvas oval id
        self.edge_lines = {}       # (v, nbr) -> canvas line id

        # ---- Control buttons ----------------------------------------
        control_frame = tk.Frame(self)
        control_frame.pack()

        btn_bfs = tk.Button(control_frame, text="Run BFS",
                            command=lambda: self.run_traversal("bfs"))
        btn_bfs.pack(side=tk.LEFT, padx=4, pady=4)

        btn_dfs = tk.Button(control_frame, text="Run DFS",
                            command=lambda: self.run_traversal("dfs"))
        btn_dfs.pack(side=tk.LEFT, padx=4, pady=4)

        btn_cycle_undirected = tk.Button(
            control_frame, text="Detect Undirected Cycle",
            command=self.run_cycle_detection)
        btn_cycle_undirected.pack(side=tk.LEFT, padx=4, pady=4)

        btn_cycle_directed = tk.Button(
            control_frame, text="Detect Directed Cycle",
            command=self.run_directed_cycle_detection)
        btn_cycle_directed.pack(side=tk.LEFT, padx=4, pady=4)

        btn_reset = tk.Button(control_frame, text="Reset Colors",
                              command=self.reset_colors)
        btn_reset.pack(side=tk.LEFT, padx=4, pady=4)

        self.info_label = tk.Label(
            self, text="", font=("Arial", 11), wraplength=640)
        self.info_label.pack(pady=6)

        self.draw_graph()

    # ------------------------------------------------------------------ #
    # Drawing helpers
    # ------------------------------------------------------------------ #

    def draw_graph(self):
        self.canvas.delete("all")
        self.vertex_positions.clear()
        self.vertex_circles.clear()
        self.edge_lines.clear()

        vertices = list(self.graph.graph.keys())
        n = len(vertices)
        if n == 0:
            return

        angle_gap = 360 / n
        cx, cy = self.center

        for i, v in enumerate(vertices):
            angle = i * angle_gap
            x = cx + self.spacing * math.cos(math.radians(angle))
            y = cy + self.spacing * math.sin(math.radians(angle))
            self.vertex_positions[v] = (x, y)

            circle_id = self.canvas.create_oval(
                x - self.node_radius, y - self.node_radius,
                x + self.node_radius, y + self.node_radius,
                fill='lightblue', outline='black', width=2)
            self.vertex_circles[v] = circle_id
            self.canvas.create_text(x, y, text=v,
                                    font=("Arial", 13, "bold"))

        for v in vertices:
            x1, y1 = self.vertex_positions[v]
            for nbr in self.graph.graph[v]:
                x2, y2 = self.vertex_positions[nbr]
                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx * dx + dy * dy)
                if dist == 0:
                    continue
                ox = dx / dist * self.node_radius
                oy = dy / dist * self.node_radius
                start = (x1 + ox, y1 + oy)
                end   = (x2 - ox, y2 - oy)

                if self.graph.directed:
                    line_id = self.canvas.create_line(
                        *start, *end, arrow=tk.LAST, width=2)
                else:
                    line_id = self.canvas.create_line(
                        *start, *end, width=2)
                self.edge_lines[(v, nbr)] = line_id

                if self.graph.weighted:
                    w = self.graph.weights.get((v, nbr), '')
                    mid_x = (start[0] + end[0]) / 2
                    mid_y = (start[1] + end[1]) / 2
                    self.canvas.create_text(mid_x, mid_y, text=str(w),
                                            fill="red",
                                            font=("Arial", 10, "italic"))

    def reset_colors(self):
        for circle_id in self.vertex_circles.values():
            self.canvas.itemconfig(circle_id, fill='lightblue')
        for line_id in self.edge_lines.values():
            self.canvas.itemconfig(line_id, fill='black', width=2)
        self.info_label.config(text="")

    def highlight_vertex(self, vertex, color):
        cid = self.vertex_circles.get(vertex)
        if cid:
            self.canvas.itemconfig(cid, fill=color)
            self.update()

    def highlight_edge(self, v1, v2, color):
        lid = self.edge_lines.get((v1, v2))
        if lid:
            self.canvas.itemconfig(lid, fill=color, width=3)
            self.update()

    # ------------------------------------------------------------------ #
    # BFS / DFS animated traversal
    # ------------------------------------------------------------------ #

    def run_traversal(self, method):
        def worker():
            self.reset_colors()
            start_vertex = ('A' if 'A' in self.graph.graph
                            else next(iter(self.graph.graph), None))
            if not start_vertex:
                self.info_label.config(text="Graph is empty")
                return

            visited = set()

            if method == "bfs":
                queue = [start_vertex]
                self.info_label.config(text="Running BFS…")
                while queue:
                    vertex = queue.pop(0)
                    if vertex not in visited:
                        self.highlight_vertex(vertex, 'orange')
                        self.info_label.config(text=f"BFS visiting: {vertex}")
                        visited.add(vertex)
                        time.sleep(0.7)
                        for nbr in self.graph.graph[vertex]:
                            if nbr not in visited and nbr not in queue:
                                queue.append(nbr)
                                self.highlight_edge(vertex, nbr, 'green')
                                time.sleep(0.3)
                self.info_label.config(text="BFS complete.")

            elif method == "dfs":
                stack = [start_vertex]
                self.info_label.config(text="Running DFS…")
                while stack:
                    vertex = stack.pop()
                    if vertex not in visited:
                        self.highlight_vertex(vertex, 'purple')
                        self.info_label.config(text=f"DFS visiting: {vertex}")
                        visited.add(vertex)
                        time.sleep(0.7)
                        for nbr in reversed(self.graph.graph[vertex]):
                            if nbr not in visited:
                                stack.append(nbr)
                                self.highlight_edge(vertex, nbr, 'blue')
                                time.sleep(0.3)
                self.info_label.config(text="DFS complete.")

        threading.Thread(target=worker, daemon=True).start()

    # ------------------------------------------------------------------ #
    # Task 8 FIX – Undirected cycle detection
    # ------------------------------------------------------------------ #

    def run_cycle_detection(self):
        def worker():
            self.reset_colors()
            if self.graph.directed:
                self.info_label.config(
                    text="Note: graph is directed – running undirected "
                         "cycle detection anyway (ignores edge direction).")
            else:
                self.info_label.config(text="Detecting cycles in undirected graph…")

            visited = set()
            has_cycle = [False]   # list so nested function can mutate it

            def cycle_dfs(current, parent):
                visited.add(current)
                self.highlight_vertex(current, 'yellow')
                self.update()
                time.sleep(0.5)
                for nbr in self.graph.graph[current]:
                    if nbr not in visited:
                        self.highlight_edge(current, nbr, 'orange')
                        self.update()
                        time.sleep(0.4)
                        if cycle_dfs(nbr, current):
                            return True
                    elif nbr != parent:
                        # Back-edge → cycle found
                        self.highlight_edge(current, nbr, 'red')
                        self.highlight_vertex(nbr, 'red')
                        self.highlight_vertex(current, 'red')
                        self.update()
                        time.sleep(0.5)
                        return True
                return False

            for vertex in self.graph.graph:
                if vertex not in visited:
                    if cycle_dfs(vertex, None):
                        has_cycle[0] = True
                        break

            if has_cycle[0]:
                self.info_label.config(text="✔ Cycle detected in the graph!")
            else:
                self.info_label.config(text="✘ No cycles found in the graph.")

        threading.Thread(target=worker, daemon=True).start()

    # ------------------------------------------------------------------ #
    # Directed cycle detection (recursion-stack DFS)
    # ------------------------------------------------------------------ #

    def run_directed_cycle_detection(self):
        def worker():
            self.reset_colors()
            if not self.graph.directed:
                self.info_label.config(
                    text="Note: graph is undirected – directed cycle "
                         "detection works best on directed graphs.")
            else:
                self.info_label.config(text="Detecting cycles in directed graph…")

            visited = set()
            rec_stack = set()
            has_cycle = [False]

            def dfs(vertex):
                visited.add(vertex)
                rec_stack.add(vertex)
                self.highlight_vertex(vertex, 'yellow')
                self.update()
                time.sleep(0.5)

                for nbr in self.graph.graph[vertex]:
                    if nbr not in visited:
                        self.highlight_edge(vertex, nbr, 'orange')
                        self.update()
                        time.sleep(0.5)
                        if dfs(nbr):
                            self.highlight_edge(vertex, nbr, 'red')
                            self.highlight_vertex(nbr, 'red')
                            self.highlight_vertex(vertex, 'red')
                            self.update()
                            time.sleep(0.5)
                            return True
                    elif nbr in rec_stack:
                        # Back-edge to ancestor → cycle
                        self.highlight_edge(vertex, nbr, 'red')
                        self.highlight_vertex(nbr, 'red')
                        self.highlight_vertex(vertex, 'red')
                        self.update()
                        time.sleep(0.5)
                        return True

                rec_stack.remove(vertex)
                return False

            for vertex in self.graph.graph:
                if vertex not in visited:
                    if dfs(vertex):
                        has_cycle[0] = True
                        break

            if has_cycle[0]:
                self.info_label.config(text="✔ Cycle detected in the directed graph!")
            else:
                self.info_label.config(text="✘ No cycles found in the directed graph.")

        threading.Thread(target=worker, daemon=True).start()


# ====================================================================== #
# Entry point – swap USE_DIRECTED to test each mode
# ====================================================================== #

if __name__ == "__main__":
    if not USE_DIRECTED:
        # ---- Undirected graph with a cycle (A-B-C-A) ----
        g = Graph(directed=False, weighted=False)
        for v in ['A', 'B', 'C', 'D']:
            g.add_vertex(v)
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('C', 'A')   # cycle
        g.add_edge('C', 'D')
        print("Launched with UNDIRECTED graph (cycle A-B-C-A).")
        print("  • 'Detect Undirected Cycle' → should find cycle")
        print("  • 'Detect Directed Cycle'   → note: undirected graph")
    else:
        # ---- Directed graph with a cycle (A→B→C→A) ----
        g = Graph(directed=True, weighted=False)
        for v in ['A', 'B', 'C', 'D']:
            g.add_vertex(v)
        g.add_edge('A', 'B')
        g.add_edge('B', 'C')
        g.add_edge('C', 'A')   # cycle
        g.add_edge('C', 'D')
        print("Launched with DIRECTED graph (cycle A→B→C→A).")
        print("  • 'Detect Undirected Cycle' → runs with direction-ignored")
        print("  • 'Detect Directed Cycle'   → should find cycle")

    app = GraphVisualizer(g)
    app.mainloop()
