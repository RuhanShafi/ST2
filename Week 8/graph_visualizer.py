from graph import Graph
import tkinter as tk
import math


class GraphVisualizer(tk.Tk):

    def __init__(self, graph):
        super().__init__()
        self.title("Graph Visualizer")
        self.geometry('650x650')
        self.graph = graph
        self.node_radius = 22
        self.spacing = 180
        self.center = (300, 280)
        self.vertex_positions = {}

        # Canvas
        self.canvas = tk.Canvas(self, width=600, height=500, bg='white')
        self.canvas.pack(pady=8)

        # Controls
        ctrl = tk.Frame(self)
        ctrl.pack(pady=4)

        tk.Label(ctrl, text="Vertex:").grid(row=0, column=0, padx=3)
        self.vertex_entry = tk.Entry(ctrl, width=4)
        self.vertex_entry.grid(row=0, column=1, padx=3)
        tk.Button(ctrl, text="Add Vertex",
                  command=self.add_vertex).grid(row=0, column=2, padx=3)
        tk.Button(ctrl, text="Remove Vertex",
                  command=self.remove_vertex).grid(row=0, column=3, padx=3)

        tk.Label(ctrl, text="Edge (v1,v2,w):").grid(row=1, column=0, padx=3, pady=4)
        self.edge_v1 = tk.Entry(ctrl, width=4)
        self.edge_v1.grid(row=1, column=1, padx=3)
        self.edge_v2 = tk.Entry(ctrl, width=4)
        self.edge_v2.grid(row=1, column=2, padx=3)
        self.edge_w = tk.Entry(ctrl, width=4)
        self.edge_w.insert(0, "0")
        self.edge_w.grid(row=1, column=3, padx=3)
        tk.Button(ctrl, text="Add Edge",
                  command=self.add_edge).grid(row=1, column=4, padx=3)
        tk.Button(ctrl, text="Remove Edge",
                  command=self.remove_edge).grid(row=1, column=5, padx=3)

        self.status = tk.Label(self, text="", fg="darkblue")
        self.status.pack()

        self.draw_graph()

    def _set_status(self, msg):
        self.status.config(text=msg)

    def add_vertex(self):
        v = self.vertex_entry.get().strip()
        if v:
            self.graph.add_vertex(v)
            self.draw_graph()
            self._set_status(f"Added vertex '{v}'")

    def remove_vertex(self):
        v = self.vertex_entry.get().strip()
        if v:
            self.graph.remove_vertex(v)
            self.draw_graph()
            self._set_status(f"Removed vertex '{v}'")

    def add_edge(self):
        v1 = self.edge_v1.get().strip()
        v2 = self.edge_v2.get().strip()
        try:
            w = int(self.edge_w.get().strip())
        except ValueError:
            w = 0
        if v1 and v2:
            self.graph.add_edge(v1, v2, w)
            self.draw_graph()
            self._set_status(f"Added edge {v1}-{v2} (w={w})")

    def remove_edge(self):
        v1 = self.edge_v1.get().strip()
        v2 = self.edge_v2.get().strip()
        if v1 and v2:
            self.graph.remove_edge(v1, v2)
            self.draw_graph()
            self._set_status(f"Removed edge {v1}-{v2}")

    def draw_graph(self):
        self.canvas.delete("all")
        self.vertex_positions.clear()

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

        # Draw edges first (so circles appear on top)
        for v in vertices:
            x1, y1 = self.vertex_positions[v]
            for nbr in self.graph.graph[v]:
                x2, y2 = self.vertex_positions[nbr]
                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx * dx + dy * dy) or 1
                ox, oy = dx / dist * self.node_radius, dy / dist * self.node_radius
                sx, sy = x1 + ox, y1 + oy
                ex, ey = x2 - ox, y2 - oy

                if self.graph.directed:
                    self.canvas.create_line(sx, sy, ex, ey, arrow=tk.LAST, width=2)
                else:
                    self.canvas.create_line(sx, sy, ex, ey, width=2)

                if self.graph.weighted:
                    w = self.graph.weights.get((v, nbr), '')
                    mx, my = (sx + ex) / 2, (sy + ey) / 2
                    self.canvas.create_text(mx, my, text=str(w),
                                            fill="red", font=("Arial", 9, "italic"))

        # Draw vertices
        for v, (x, y) in self.vertex_positions.items():
            r = self.node_radius
            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill='lightblue', outline='black', width=2)
            self.canvas.create_text(x, y, text=v, font=("Arial", 12, "bold"))


if __name__ == "__main__":
    g = Graph(directed=True, weighted=True)
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.add_edge('A', 'B', 10)
    g.add_edge('B', 'C', 20)
    g.add_edge('C', 'A', 30)
    app = GraphVisualizer(g)
    app.mainloop()
