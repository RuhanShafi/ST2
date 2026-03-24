
import tkinter as tk
from tkinter import messagebox

NODE_WIDTH = 60
NODE_HEIGHT = 40
HORIZONTAL_GAP = 40
CANVAS_HEIGHT = 120
CANVAS_WIDTH = 900

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    
    def insert_at_index(self, data, index):
        new_node = Node(data)
        if index == 0:
            if self.head:
                new_node.next = self.head
                self.head.prev = new_node
            self.head = new_node
            return True

        current = self.head
        count = 0
        while current and count < index:
            prev = current
            current = current.next
            count += 1
        
        if count == index:
            new_node.next = current
            new_node.prev = prev
            prev.next = new_node
            if current:
                current.prev = new_node
            return True
        else:
            return False

    def delete_value(self, value):
        current = self.head
        while current:
            if current.data == value:
                if current.prev:
                    current.prev.next = current.next
                else:   # deleting head
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def search(self, value):
        current = self.head
        index = 0
        while current:
            if current.data == value:
                return index
            current = current.next
            index += 1
        return -1

    def to_list(self):
        arr = []
        current = self.head
        while current:
            arr.append(current.data)
            current = current.next
        return arr

class DoublyLinkedListVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Doubly Linked List Visualizer")

        self.dll = DoublyLinkedList()

        # UI Setup
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack(pady=20)

        control_frame = tk.Frame(root)
        control_frame.pack()

        # Insert controls
        tk.Label(control_frame, text="Insert Value:").grid(row=0, column=0)
        self.insert_value_entry = tk.Entry(control_frame, width=5)
        self.insert_value_entry.grid(row=0, column=1)

        tk.Label(control_frame, text="at Index:").grid(row=0, column=2)
        self.insert_index_entry = tk.Entry(control_frame, width=5)
        self.insert_index_entry.grid(row=0, column=3)

        insert_btn = tk.Button(control_frame, text="Insert", command=self.insert_node)
        insert_btn.grid(row=0, column=4, padx=10)

        # Delete controls
        tk.Label(control_frame, text="Delete Value:").grid(row=1, column=0)
        self.delete_value_entry = tk.Entry(control_frame, width=5)
        self.delete_value_entry.grid(row=1, column=1)
        delete_btn = tk.Button(control_frame, text="Delete", command=self.delete_node)
        delete_btn.grid(row=1, column=4, padx=10)

        # Search controls
        tk.Label(control_frame, text="Search Value:").grid(row=2, column=0)
        self.search_value_entry = tk.Entry(control_frame, width=5)
        self.search_value_entry.grid(row=2, column=1)
        search_btn = tk.Button(control_frame, text="Search", command=self.search_node)
        search_btn.grid(row=2, column=4, padx=10)

        self.status_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.status_label.pack(pady=10)

        self.draw_list()

    def draw_node(self, x, y, data, highlight=False):
        fill_color = "yellow" if highlight else "lightgrey"
        outline_color = "red" if highlight else "black"

        # Draw rectangle for node
        self.canvas.create_rectangle(x, y, x + NODE_WIDTH, y + NODE_HEIGHT,
                                     fill=fill_color, outline=outline_color, width=2)
        # Draw value text centered
        self.canvas.create_text(x + NODE_WIDTH // 2, y + NODE_HEIGHT // 2,
                                text=str(data), font=("Arial", 16))

    def draw_arrow(self, x1, y1, x2, y2):
        # Draw simple arrow line with arrowhead at (x2,y2)
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2)

    def draw_double_arrow(self, x1, y1, x2, y2):
        # Draw two arrows pointing opposite directions between x1,y1 and x2,y2
        self.canvas.create_line(x1, y1, x2, y2, arrow=tk.BOTH, width=2)

    def draw_list(self, highlight_index=None):
        self.canvas.delete("all")
        nodes = self.dll.to_list()
        x = 20
        y = 40

        # Keep coordinates of centers to draw arrows between nodes
        centers = []

        # Draw nodes
        for i, val in enumerate(nodes):
            highlight = (i == highlight_index)
            self.draw_node(x, y, val, highlight)
            centers.append((x + NODE_WIDTH // 2, y + NODE_HEIGHT // 2))
            x += NODE_WIDTH + HORIZONTAL_GAP

        # Draw arrows (both ways)
        for i in range(len(centers) - 1):
            x1, y1 = centers[i]
            x2, y2 = centers[i + 1]
            # Arrow from node i to i+1 (forward)
            self.draw_arrow(x1 + 15, y1, x2 - 15, y2)
            # Arrow from node i+1 to i (backward)
            self.draw_arrow(x2 - 15, y2 + 10, x1 + 15, y1 + 10)

    def insert_node(self):
        try:
            val = int(self.insert_value_entry.get())
            index = int(self.insert_index_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers for value and index.")
            return
        if index < 0:
            messagebox.showerror("Input Error", "Index must be non-negative.")
            return
        success = self.dll.insert_at_index(val, index)
        if not success:
            messagebox.showerror("Index Error", "Index out of range.")
            return
        self.status_label.config(text=f"Inserted {val} at index {index}")
        self.draw_list()

    def delete_node(self):
        try:
            val = int(self.delete_value_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer value to delete.")
            return
        success = self.dll.delete_value(val)
        if success:
            self.status_label.config(text=f"Deleted value {val} from the list")
            self.draw_list()
        else:
            messagebox.showinfo("Not Found", f"Value {val} not found.")

    def search_node(self):
        try:
            val = int(self.search_value_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer value to search.")
            return

        nodes = self.dll.to_list()
        found_index = -1

        def highlight_next(i=0):
            if i > 0:
                self.draw_list()
            if i < len(nodes):
                self.draw_list(highlight_index=i)
                if nodes[i] == val:
                    self.status_label.config(text=f"Value {val} found at index {i}")
                    return
                self.root.after(500, lambda: highlight_next(i + 1))
            else:
                self.status_label.config(text=f"Value {val} not found in the list")
                self.draw_list()

        highlight_next()

if __name__ == "__main__":
    root = tk.Tk()
    app = DoublyLinkedListVisualizer(root)

    # Optional: Pre-populate list
    for v in [10, 20, 30, 40]:
        app.dll.insert_at_index(v, app.dll.search(v)+1 if app.dll.search(v) != -1 else 100)  # Insert at end
    app.draw_list()

    root.mainloop()

#linked_lists_practice.py

import time
import random

# Singly Linked List Node and Class
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
    
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_index(self, data, index):
        new_node = Node(data)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return True
        current = self.head
        prev = None
        count = 0
        while current and count < index:
            prev = current
            current = current.next
            count += 1
        if count == index:
            prev.next = new_node
            new_node.next = current
            return True
        else:
            return False
    
    def search(self, val):
        current = self.head
        while current:
            if current.data == val:
                return True
            current = current.next
        return False
    
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


# Doubly Linked List Node and Class
class DNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
    
    def insert_at_index(self, data, index):
        new_node = DNode(data)
        if index == 0:
            if self.head:
                new_node.next = self.head
                self.head.prev = new_node
            self.head = new_node
            return True
        current = self.head
        count = 0
        while current and count < index:
            prev = current
            current = current.next
            count += 1
        if count == index:
            new_node.next = current
            new_node.prev = prev
            prev.next = new_node
            if current:
                current.prev = new_node
            return True
        return False

    def search(self, val):
        current = self.head
        while current:
            if current.data == val:
                return True
            current = current.next
        return False

    def delete_value(self, val):
        current = self.head
        while current:
            if current.data == val:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

# Timer utility
def time_operation(func, *args, repeats=5):
    times = []
    for _ in range(repeats):
        start = time.time()
        func(*args)
        end = time.time()
        times.append(end - start)
    avg = sum(times) / repeats
    return avg

# Test functions for each DS
def test_list_insert(lst, data, index):
    lst.insert(index, data)

def test_list_search(lst, val):
    return val in lst

def test_list_delete(lst, val):
    try:
        lst.remove(val)
    except ValueError:
        pass

def test_sll_insert(sll, data, index):
    sll.insert_at_index(data, index)

def test_sll_search(sll, val):
    return sll.search(val)

def test_sll_delete(sll, val):
    sll.delete_value(val)

def test_dll_insert(dll, data, index):
    dll.insert_at_index(data, index)

def test_dll_search(dll, val):
    return dll.search(val)

def test_dll_delete(dll, val):
    dll.delete_value(val)

def build_sll(data_list):
    sll = SinglyLinkedList()
    for i, val in enumerate(data_list):
        sll.insert_at_index(val, i)
    return sll

def build_dll(data_list):
    dll = DoublyLinkedList()
    for i, val in enumerate(data_list):
        dll.insert_at_index(val, i)
    return dll

#Testing

def main():
    size = 1000
    data = [random.randint(1, 10**6) for _ in range(size)]
    mid_index = size // 2
    search_val = data[mid_index]

    print(f"Testing with {size} elements, search and delete value: {search_val}")

    ### Python list tests
    pylist = data.copy()
    
    insert_time = time_operation(test_list_insert, pylist, -1, 0)
    search_time = time_operation(test_list_search, pylist, search_val)
    delete_time = time_operation(test_list_delete, pylist, search_val)

    print(f"Python list insert at beginning: {insert_time:.6f} s")
    print(f"Python list search: {search_time:.6f} s")
    print(f"Python list delete: {delete_time:.6f} s")

    ### Singly Linked List tests
    sll = build_sll(data)
    
    insert_time = time_operation(test_sll_insert, sll, -1, 0)
    search_time = time_operation(test_sll_search, sll, search_val)
    delete_time = time_operation(test_sll_delete, sll, search_val)

    print(f"Singly Linked List insert at beginning: {insert_time:.6f} s")
    print(f"Singly Linked List search: {search_time:.6f} s")
    print(f"Singly Linked List delete: {delete_time:.6f} s")

    ### Doubly Linked List tests
    dll = build_dll(data)
    
    insert_time = time_operation(test_dll_insert, dll, -1, 0)
    search_time = time_operation(test_dll_search, dll, search_val)
    delete_time = time_operation(test_dll_delete, dll, search_val)

    print(f"Doubly Linked List insert at beginning: {insert_time:.6f} s")
    print(f"Doubly Linked List search: {search_time:.6f} s")
    print(f"Doubly Linked List delete: {delete_time:.6f} s")

if __name__ == "__main__":
    main()


#priority_queue_visualiser.py
import tkinter as tk
from tkinter import messagebox
import heapq

NODE_WIDTH = 60
NODE_HEIGHT = 40
HORIZONTAL_GAP = 10
VERTICAL_GAP = 50
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 400

class PriorityQueueVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority Queue Visualizer")

        self.heap = []

        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack(pady=20)

        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Label(control_frame, text="Add Task (priority,value):").grid(row=0, column=0)
        self.task_entry = tk.Entry(control_frame, width=20)
        self.task_entry.grid(row=0, column=1)

        add_btn = tk.Button(control_frame, text="Add Task", command=self.add_task)
        add_btn.grid(row=0, column=2, padx=5)

        pop_btn = tk.Button(control_frame, text="Pop Task", command=self.pop_task)
        pop_btn.grid(row=1, column=2, pady=5)

        self.status_label = tk.Label(root, text="", fg="blue", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.draw_heap()

    def draw_node(self, x, y, val):
        rect = self.canvas.create_rectangle(x, y, x + NODE_WIDTH, y + NODE_HEIGHT,
                                            fill="orange", outline="black", width=2)
        self.canvas.create_text(x + NODE_WIDTH/2, y + NODE_HEIGHT/2, text=str(val), font=("Arial", 14))
        return rect

    def draw_lines(self, x1, y1, x2, y2):
        self.canvas.create_line(x1 + NODE_WIDTH/2, y1 + NODE_HEIGHT, x2 + NODE_WIDTH/2, y2, width=2)

    def draw_heap(self):
        self.canvas.delete("all")
        if not self.heap:
            return
        # Draw nodes in tree-like structure
        level_indices = [0]
        level = 0
        y = 20
        # Calculate positions
        positions = {}
        width = CANVAS_WIDTH

        def calc_x(i, level):
            gaps = 2 ** (level + 1)
            pos = (i * width) // gaps + width // (2 * gaps)
            return pos

        i = 0
        while i < len(self.heap):
            nodes_this_level = 2 ** level
            for j in range(nodes_this_level):
                if i >= len(self.heap):
                    break
                x = calc_x(j, level)
                positions[i] = (x, y)
                i += 1
            y += VERTICAL_GAP
            level += 1

        # Draw lines (parent->child)
        for i in range(len(self.heap)):
            left = 2*i + 1
            right = 2*i + 2
            if left < len(self.heap):
                x1, y1 = positions[i]
                x2, y2 = positions[left]
                self.draw_lines(x1, y1, x2, y2)
            if right < len(self.heap):
                x1, y1 = positions[i]
                x2, y2 = positions[right]
                self.draw_lines(x1, y1, x2, y2)

        # Draw nodes
        for i, val in enumerate(self.heap):
            x, y = positions[i]
            self.draw_node(x, y, val)

    def add_task(self):
        val = self.task_entry.get()
        try:
            # Expect input as "priority,value"
            prio_str, task_val = val.split(',')
            prio = int(prio_str.strip())
            task_val = task_val.strip()
        except Exception:
            messagebox.showerror("Input Error", "Input should be in 'priority,value' format. Example: 2,TaskA")
            return
        heapq.heappush(self.heap, (prio, task_val))
        self.task_entry.delete(0, tk.END)
        self.status_label.config(text=f"Added task '{task_val}' with priority {prio}")
        self.draw_heap()

    def pop_task(self):
        if not self.heap:
            messagebox.showinfo("Empty Queue", "No tasks available to pop.")
            return
        prio, task = heapq.heappop(self.heap)
        self.status_label.config(text=f"Popped task '{task}' with priority {prio}")
        self.draw_heap()

if __name__ == "__main__":
    root = tk.Tk()
    app = PriorityQueueVisualizer(root)

    # Example test cases:
    # heapq.heappush(app.heap, (1,"Eat"))
    # heapq.heappush(app.heap, (3,"Sleep"))
    # heapq.heappush(app.heap, (2,"Work"))
    # app.draw_heap()

    root.mainloop()

#stack_visualiser.py
import tkinter as tk
from tkinter import messagebox

NODE_WIDTH = 80
NODE_HEIGHT = 40
VERTICAL_GAP = 10
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 500

class StackVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Visualizer")

        self.stack = []

        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='white')
        self.canvas.pack(pady=20)

        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Label(control_frame, text="Push Value:").grid(row=0, column=0)
        self.push_entry = tk.Entry(control_frame, width=10)
        self.push_entry.grid(row=0, column=1)

        push_btn = tk.Button(control_frame, text="Push", command=self.push_value)
        push_btn.grid(row=0, column=2, padx=5)

        pop_btn = tk.Button(control_frame, text="Pop", command=self.pop_value)
        pop_btn.grid(row=1, column=2, pady=5)

        self.status_label = tk.Label(root, text="", fg="blue", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.draw_stack()

    def draw_node(self, x, y, data):
        rect = self.canvas.create_rectangle(x, y, x + NODE_WIDTH, y + NODE_HEIGHT, fill="lightblue", outline="black", width=2)
        self.canvas.create_text(x + NODE_WIDTH/2, y + NODE_HEIGHT/2, text=str(data), font=("Arial", 16))
        return rect

    def draw_stack(self):
        self.canvas.delete("all")
        x = (CANVAS_WIDTH - NODE_WIDTH) // 2
        y = CANVAS_HEIGHT - NODE_HEIGHT - 10
        for val in reversed(self.stack):
            self.draw_node(x, y, val)
            y -= NODE_HEIGHT + VERTICAL_GAP
        # Draw label for top
        if self.stack:
            self.canvas.create_text(x + NODE_WIDTH + 40, CANVAS_HEIGHT - NODE_HEIGHT - 10, text="Top", font=("Arial", 12), fill="red")

    def push_value(self):
        try:
            val = int(self.push_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer value to push.")
            return
        self.stack.append(val)
        self.push_entry.delete(0, tk.END)
        self.status_label.config(text=f"Pushed {val} onto stack")
        self.draw_stack()

    def pop_value(self):
        if len(self.stack) == 0:
            messagebox.showinfo("Empty Stack", "Stack is empty. Cannot pop.")
            return
        val = self.stack.pop()
        self.status_label.config(text=f"Popped {val} from stack")
        self.draw_stack()

if __name__ == "__main__":
    root = tk.Tk()
    app = StackVisualizer(root)

    # Example test cases:
    # app.stack = [10, 20, 30]
    # app.draw_stack()
    root.mainloop()

#stacks_queues_practice.py
import time
import random
from collections import deque
import heapq

# Timer utility
def time_operation(func, *args, repeats=5):
    times = []
    for _ in range(repeats):
        start = time.time()
        func(*args)
        end = time.time()
        times.append(end - start)
    avg = sum(times) / repeats
    return avg

# Stack operations using list
def stack_push(stack, values):
    for val in values:
        stack.append(val)

def stack_pop(stack, count):
    for _ in range(count):
        if stack:
            stack.pop()

def stack_peek(stack):
    return stack[-1] if stack else None

# Queue operations using deque
def queue_enqueue(queue, values):
    for val in values:
        queue.append(val)

def queue_dequeue(queue, count):
    for _ in range(count):
        if queue:
            queue.popleft()

def queue_peek(queue):
    return queue[0] if queue else None

# Priority Queue operations using heapq
def pq_push(pq, values):
    for val in values:
        heapq.heappush(pq, val)

def pq_pop(pq, count):
    for _ in range(count):
        if pq:
            heapq.heappop(pq)

def pq_peek(pq):
    return pq[0] if pq else None

def main():
    size = 1000
    values = [random.randint(1, 10**6) for _ in range(size)]

    print(f"Benchmarking with {size} values")

    # Stack benchmark
    stack = []
    t_push = time_operation(stack_push, stack, values)
    t_peek = time_operation(stack_peek, stack)
    t_pop = time_operation(stack_pop, stack, size)
    print(f"Stack (list) Push: {t_push:.6f} s")
    print(f"Stack (list) Peek: {t_peek:.6f} s")
    print(f"Stack (list) Pop: {t_pop:.6f} s")

    # Queue benchmark
    queue = deque()
    t_enqueue = time_operation(queue_enqueue, queue, values)
    t_peek = time_operation(queue_peek, queue)
    t_dequeue = time_operation(queue_dequeue, queue, size)
    print(f"Queue (deque) Enqueue: {t_enqueue:.6f} s")
    print(f"Queue (deque) Peek: {t_peek:.6f} s")
    print(f"Queue (deque) Dequeue: {t_dequeue:.6f} s")

    # Priority Queue benchmark
    pq = []
    t_push = time_operation(pq_push, pq, values)
    t_peek = time_operation(pq_peek, pq)
    t_pop = time_operation(pq_pop, pq, size)
    print(f"Priority Queue (heapq) Push: {t_push:.6f} s")
    print(f"Priority Queue (heapq) Peek: {t_peek:.6f} s")
    print(f"Priority Queue (heapq) Pop: {t_pop:.6f} s")

if __name__ == "__main__":
    main()
