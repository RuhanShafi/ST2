import tkinter as tk
from tkinter import messagebox

NODE_WIDTH = 60
NODE_HEIGHT = 40
HORIZONTAL_GAP = 20


class QueueVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue Visualizer (FIFO)")

        self.queue = []

        # Canvas
        self.canvas = tk.Canvas(root, width=900, height=200)
        self.canvas.pack(pady=20)

        # Controls
        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="Value").grid(row=0, column=0)
        self.entry = tk.Entry(frame, width=10)
        self.entry.grid(row=0, column=1)

        tk.Button(frame, text="Push", command=self.enqueue).grid(row=0, column=2)
        tk.Button(frame, text="Pop", command=self.dequeue).grid(row=0, column=3)

        # Status
        self.status = tk.Label(root, text="")
        self.status.pack()

        self.draw()

    # -----------------------------
    # DRAW QUEUE
    # -----------------------------
    def draw(self):
        self.canvas.delete("all")

        x = 50
        y = 80

        for i, val in enumerate(self.queue):
            # Draw node
            self.canvas.create_rectangle(x, y, x + NODE_WIDTH, y + NODE_HEIGHT)
            self.canvas.create_text(x + 30, y + 20, text=str(val))

            # Labels
            if i == 0:
                self.canvas.create_text(x + 30, y - 20, text="FRONT", fill="blue")

            if i == len(self.queue) - 1:
                self.canvas.create_text(x + 30, y + 60, text="REAR", fill="green")

            x += NODE_WIDTH + HORIZONTAL_GAP

    # -----------------------------
    # ENQUEUE
    # -----------------------------
    def enqueue(self):
        try:
            val = int(self.entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid integer")
            return

        self.queue.append(val)
        self.status.config(text=f"Pushed {val}")
        self.draw()

    # -----------------------------
    # DEQUEUE
    # -----------------------------
    def dequeue(self):
        try:
            val = int(self.entry.get())
        except:
            messagebox.showerror("Error", "Enter a valid integer")
            return

        if val not in self.queue:
            messagebox.showerror("Error", "Value not found in queue")
            return

        self.queue.remove(val)
        self.status.config(text=f"Popped {val} from queue")
        self.draw()


# -----------------------------
# MAIN
# -----------------------------
root = tk.Tk()
app = QueueVisualizer(root)
root.mainloop()