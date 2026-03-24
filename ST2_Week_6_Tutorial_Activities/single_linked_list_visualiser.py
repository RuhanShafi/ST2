import tkinter as tk
from tkinter import messagebox

NODE_WIDTH = 60
NODE_HEIGHT = 40
HORIZONTAL_GAP = 40

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_index(self, data, index):
        new = Node(data)

        if index == 0:
            new.next = self.head
            self.head = new
            return True

        current = self.head
        count = 0

        while current and count < index - 1:
            current = current.next
            count += 1

        if current is None:
            return False

        new.next = current.next
        current.next = new
        return True

    def delete_value(self, val):
        current = self.head
        prev = None

        while current:
            if current.data == val:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def search(self, val):
        current = self.head
        index = 0

        while current:
            if current.data == val:
                return index
            current = current.next
            index += 1

        return -1

    def to_list(self):
        arr = []
        cur = self.head
        while cur:
            arr.append(cur.data)
            cur = cur.next
        return arr


class Visualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Singly Linked List Visualizer")

        self.list = SinglyLinkedList()

        self.canvas = tk.Canvas(root, width=900, height=150)
        self.canvas.pack(pady=20)

        frame = tk.Frame(root)
        frame.pack()

        tk.Label(frame, text="Value").grid(row=0, column=0)
        self.val_entry = tk.Entry(frame, width=5)
        self.val_entry.grid(row=0, column=1)

        tk.Label(frame, text="Index").grid(row=0, column=2)
        self.idx_entry = tk.Entry(frame, width=5)
        self.idx_entry.grid(row=0, column=3)

        tk.Button(frame, text="Insert", command=self.insert).grid(row=0, column=4)
        tk.Button(frame, text="Delete", command=self.delete).grid(row=1, column=4)
        tk.Button(frame, text="Search", command=self.search).grid(row=2, column=4)

        self.status = tk.Label(root, text="")
        self.status.pack()

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        x = 20
        y = 50

        nodes = self.list.to_list()

        for i, val in enumerate(nodes):
            self.canvas.create_rectangle(x, y, x+NODE_WIDTH, y+NODE_HEIGHT)
            self.canvas.create_text(x+30, y+20, text=str(val))

            if i < len(nodes) - 1:
                self.canvas.create_line(x+60, y+20, x+100, y+20, arrow=tk.LAST)

            x += NODE_WIDTH + HORIZONTAL_GAP

    def insert(self):
        try:
            val = int(self.val_entry.get())
            idx = int(self.idx_entry.get())
        except:
            messagebox.showerror("Error", "Invalid input")
            return

        if not self.list.insert_at_index(val, idx):
            messagebox.showerror("Error", "Index out of range")
        else:
            self.status.config(text=f"Inserted {val} at index {idx}")
            self.draw()

    def delete(self):
        val = int(self.val_entry.get())
        if self.list.delete_value(val):
            self.status.config(text=f"Deleted {val}")
            self.draw()
        else:
            messagebox.showerror("Error", "Value not found")

    def search(self):
        val = int(self.val_entry.get())
        idx = self.list.search(val)

        if idx != -1:
            self.status.config(text=f"Found at index {idx}")
        else:
            self.status.config(text="Not found")


root = tk.Tk()
Visualizer(root)
root.mainloop()