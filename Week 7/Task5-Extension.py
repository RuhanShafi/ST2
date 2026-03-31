import tkinter as tk
from tkinter import messagebox, ttk
import time
import random
import string
import matplotlib.pyplot as plt


# ===== Colour Constants =====

RED = True
BLACK = False


# ===== Red-Black Tree Node =====

class RBNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None
        self.parent = None
        self.color = RED  # New nodes are always red


# ===== Red-Black Tree Class =====

class RedBlackTree:
    """
    Red-Black Tree Properties:
      1. Each node is red or black.
      2. The root is always black.
      3. Red nodes cannot have red children (no two reds in a row).
      4. Every path from a node to a leaf (None) has the same number of black nodes.
    """

    def __init__(self):
        # Sentinel NIL node (black)
        self.NIL = RBNode(None, None)
        self.NIL.color = BLACK
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.root = self.NIL

    # ===== Rotations =====

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    # ===== Insertion =====

    def insert(self, name, phone):
        # Create new node
        node = RBNode(name, phone)
        node.left = self.NIL
        node.right = self.NIL
        node.parent = None
        node.color = RED

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if node.name < current.name:
                current = current.left
            elif node.name > current.name:
                current = current.right
            else:
                # Update existing
                current.phone = phone
                return

        node.parent = parent

        if parent is None:
            self.root = node
        elif node.name < parent.name:
            parent.left = node
        else:
            parent.right = node

        # Fix Red-Black Tree violations
        self._insert_fix(node)

    def _insert_fix(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # Uncle
                if y.color == RED:
                    # Case 1: Uncle is red → recolour
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # Case 2: Triangle → rotate to make Case 3
                        z = z.parent
                        self._left_rotate(z)
                    # Case 3: Line → rotate and recolour
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left  # Uncle
                if y.color == RED:
                    # Case 1 (mirror)
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        # Case 2 (mirror)
                        z = z.parent
                        self._right_rotate(z)
                    # Case 3 (mirror)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)

        self.root.color = BLACK

    # ===== Search =====

    def search(self, name):
        return self._search_node(self.root, name)

    def _search_node(self, node, name):
        if node == self.NIL or node.name == name:
            return node if node != self.NIL else None
        if name < node.name:
            return self._search_node(node.left, name)
        else:
            return self._search_node(node.right, name)

    # ===== Deletion =====

    def delete(self, name):
        z = self._find_node(self.root, name)
        if z == self.NIL or z is None:
            return
        self._delete_node(z)

    def _find_node(self, node, name):
        if node == self.NIL:
            return self.NIL
        if name == node.name:
            return node
        elif name < node.name:
            return self._find_node(node.left, name)
        else:
            return self._find_node(node.right, name)

    def _minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_node(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == BLACK:
            self._delete_fix(x)

    def _delete_fix(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    # ===== Inorder Traversal =====

    def inorder(self):
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node != self.NIL:
            self._inorder_helper(node.left, result)
            result.append((node.name, node.phone))
            self._inorder_helper(node.right, result)


# ===== BST (reused from Task 4) =====

class BSTNode:
    def __init__(self, name, phone=None):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, name, phone):
        if root is None:
            return BSTNode(name, phone)
        if name < root.name:
            root.left = self.insert(root.left, name, phone)
        elif name > root.name:
            root.right = self.insert(root.right, name, phone)
        else:
            root.phone = phone
        return root

    def search(self, root, name):
        if root is None or root.name == name:
            return root
        if name < root.name:
            return self.search(root.left, name)
        return self.search(root.right, name)

    def find_min(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def delete(self, root, name):
        if root is None:
            return root
        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.find_min(root.right)
            root.name = temp.name
            root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)
        return root


# ===== AVL Tree (reused from Task 4) =====

class AVLNode:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def right_rotate(self, z):
        y = z.left; T3 = y.right
        y.right = z; z.left = T3
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def left_rotate(self, z):
        y = z.right; T2 = y.left
        y.left = z; z.right = T2
        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, node, name, phone):
        if not node:
            return AVLNode(name, phone)
        if name < node.name:
            node.left = self.insert(node.left, name, phone)
        elif name > node.name:
            node.right = self.insert(node.right, name, phone)
        else:
            node.phone = phone; return node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and name < node.left.name:
            return self.right_rotate(node)
        if balance < -1 and name > node.right.name:
            return self.left_rotate(node)
        if balance > 1 and name > node.left.name:
            node.left = self.left_rotate(node.left); return self.right_rotate(node)
        if balance < -1 and name < node.right.name:
            node.right = self.right_rotate(node.right); return self.left_rotate(node)
        return node

    def min_value_node(self, node):
        while node.left: node = node.left
        return node

    def delete(self, root, name):
        if not root: return root
        if name < root.name:
            root.left = self.delete(root.left, name)
        elif name > root.name:
            root.right = self.delete(root.right, name)
        else:
            if root.left is None: return root.right
            if root.right is None: return root.left
            temp = self.min_value_node(root.right)
            root.name = temp.name; root.phone = temp.phone
            root.right = self.delete(root.right, temp.name)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left); return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right); return self.left_rotate(root)
        return root

    def search(self, node, name):
        if node is None or node.name == name: return node
        if name < node.name: return self.search(node.left, name)
        return self.search(node.right, name)


# ===== Red-Black Tree GUI App =====

class RBTreeApp:
    def __init__(self, master):
        self.rbt = RedBlackTree()
        self.master = master
        master.title("Red-Black Tree Contact Directory")

        # Input frame
        frame = tk.Frame(master)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0, padx=5)
        self.name_entry = tk.Entry(frame)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5)
        self.phone_entry = tk.Entry(frame)
        self.phone_entry.grid(row=1, column=1, padx=5)

        # Buttons
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Insert", command=self.insert_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Search", command=self.search_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_contact).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Show All", command=self.show_all).grid(row=0, column=3, padx=5)

        # Output text
        self.output_text = tk.Text(master, height=10, width=60)
        self.output_text.pack(pady=10)

        # Canvas for tree visualisation
        self.canvas = tk.Canvas(master, width=900, height=450, bg="white")
        self.canvas.pack(pady=10)

        # Legend
        legend = tk.Frame(master)
        legend.pack()
        tk.Label(legend, text="●", fg="red", font=("Arial", 14)).grid(row=0, column=0)
        tk.Label(legend, text="Red Node  ").grid(row=0, column=1)
        tk.Label(legend, text="●", fg="black", font=("Arial", 14)).grid(row=0, column=2)
        tk.Label(legend, text="Black Node").grid(row=0, column=3)

    def insert_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Input Error", "Please enter both Name and Phone.")
            return
        self.rbt.insert(name, phone)
        messagebox.showinfo("Success", f"Inserted/Updated contact: {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def search_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a Name to search.")
            return
        node = self.rbt.search(name)
        self.output_text.delete(1.0, tk.END)
        if node:
            self.output_text.insert(tk.END, f"Found Contact:\nName: {node.name}\nPhone: {node.phone}\n")
        else:
            self.output_text.insert(tk.END, "Contact not found.\n")

    def delete_contact(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a Name to delete.")
            return
        self.rbt.delete(name)
        messagebox.showinfo("Success", f"Deleted contact (if existed): {name}")
        self.clear_entries()
        self.show_all()
        self.draw_tree()

    def show_all(self):
        self.output_text.delete(1.0, tk.END)
        contacts = self.rbt.inorder()
        if not contacts:
            self.output_text.insert(tk.END, "No contacts found.\n")
        else:
            for name, phone in contacts:
                self.output_text.insert(tk.END, f"Name: {name}, Phone: {phone}\n")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def draw_tree(self):
        self.canvas.delete("all")
        if self.rbt.root == self.rbt.NIL:
            return
        width = self.canvas.winfo_width() or 900
        self._draw_node(self.rbt.root, width // 2, 30, width // 4)

    def _draw_node(self, node, x, y, x_offset):
        if node == self.rbt.NIL:
            return
        radius = 22
        fill_color = "tomato" if node.color == RED else "gray20"
        text_color = "white"

        # Draw edges to children first
        if node.left != self.rbt.NIL:
            x_left = x - x_offset
            y_left = y + 75
            self.canvas.create_line(x, y + radius, x_left, y_left - radius, width=2)
            self._draw_node(node.left, x_left, y_left, max(x_offset // 2, 20))

        if node.right != self.rbt.NIL:
            x_right = x + x_offset
            y_right = y + 75
            self.canvas.create_line(x, y + radius, x_right, y_right - radius, width=2)
            self._draw_node(node.right, x_right, y_right, max(x_offset // 2, 20))

        # Draw node
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=fill_color, outline="black", width=2)
        display_name = node.name if len(node.name) <= 8 else node.name[:8] + ".."
        self.canvas.create_text(x, y, text=display_name,
                                fill=text_color, font=("Arial", 9, "bold"))


# ===== Benchmarking: BST vs AVL vs Red-Black Tree =====

def benchmark_three_trees(n=1000, search_fraction=0.5, delete_count=100, verbose=True):
    names = [''.join(random.choices(string.ascii_lowercase, k=10)) for _ in range(n)]
    phones = [''.join(random.choices(string.digits, k=10)) for _ in range(n)]
    search_names = (random.sample(names, int(n * search_fraction))
                    + ['notfoundname'] * int(n * (1 - search_fraction)))
    delete_names = random.sample(names, delete_count)

    results = {}

    # --- BST ---
    bst = BST()
    start = time.time()
    for i in range(n):
        bst.root = bst.insert(bst.root, names[i], phones[i])
    bst_insert = time.time() - start

    start = time.time()
    found_bst = sum(1 for name in search_names if bst.search(bst.root, name))
    bst_search = time.time() - start

    start = time.time()
    for name in delete_names:
        bst.root = bst.delete(bst.root, name)
    bst_delete = time.time() - start

    results['BST'] = {'insert': bst_insert, 'search': bst_search, 'delete': bst_delete, 'found': found_bst}

    # --- AVL ---
    avl = AVLTree()
    start = time.time()
    for i in range(n):
        avl.root = avl.insert(avl.root, names[i], phones[i])
    avl_insert = time.time() - start

    start = time.time()
    found_avl = sum(1 for name in search_names if avl.search(avl.root, name))
    avl_search = time.time() - start

    start = time.time()
    for name in delete_names:
        avl.root = avl.delete(avl.root, name)
    avl_delete = time.time() - start

    results['AVL'] = {'insert': avl_insert, 'search': avl_search, 'delete': avl_delete, 'found': found_avl}

    # --- Red-Black Tree ---
    rbt = RedBlackTree()
    start = time.time()
    for i in range(n):
        rbt.insert(names[i], phones[i])
    rbt_insert = time.time() - start

    start = time.time()
    found_rbt = sum(1 for name in search_names if rbt.search(name))
    rbt_search = time.time() - start

    start = time.time()
    for name in delete_names:
        rbt.delete(name)
    rbt_delete = time.time() - start

    results['RBT'] = {'insert': rbt_insert, 'search': rbt_search, 'delete': rbt_delete, 'found': found_rbt}

    if verbose:
        print(f"\nBenchmark Results (N={n}):")
        print(f"{'Operation':<12} {'BST':>12} {'AVL':>12} {'RBT':>12}")
        print("-" * 50)
        print(f"{'Insert':<12} {bst_insert:>12.6f} {avl_insert:>12.6f} {rbt_insert:>12.6f}")
        print(f"{'Search':<12} {bst_search:>12.6f} {avl_search:>12.6f} {rbt_search:>12.6f}")
        print(f"{'Delete':<12} {bst_delete:>12.6f} {avl_delete:>12.6f} {rbt_delete:>12.6f}")
        print(f"\nFound in search: BST={found_bst}, AVL={found_avl}, RBT={found_rbt} / {len(search_names)}")

    return results


def benchmark_three_trees_for_sizes(sizes, num_search=100, num_delete=50):
    """Plot BST vs AVL vs RBT performance across different data sizes."""
    bst_times = {'insert': [], 'search': [], 'delete': []}
    avl_times = {'insert': [], 'search': [], 'delete': []}
    rbt_times = {'insert': [], 'search': [], 'delete': []}

    for n in sizes:
        names = [''.join(random.choices(string.ascii_lowercase, k=8)) for _ in range(n)]
        phones = [''.join(random.choices(string.digits, k=10)) for _ in range(n)]
        search_names = random.sample(names, min(num_search, n))
        delete_names = random.sample(names, min(num_delete, n))

        # BST
        bst = BST()
        start = time.time()
        for i in range(n): bst.root = bst.insert(bst.root, names[i], phones[i])
        bst_times['insert'].append(time.time() - start)
        start = time.time()
        for name in search_names: bst.search(bst.root, name)
        bst_times['search'].append(time.time() - start)
        start = time.time()
        for name in delete_names: bst.root = bst.delete(bst.root, name)
        bst_times['delete'].append(time.time() - start)

        # AVL
        avl = AVLTree()
        start = time.time()
        for i in range(n): avl.root = avl.insert(avl.root, names[i], phones[i])
        avl_times['insert'].append(time.time() - start)
        start = time.time()
        for name in search_names: avl.search(avl.root, name)
        avl_times['search'].append(time.time() - start)
        start = time.time()
        for name in delete_names: avl.root = avl.delete(avl.root, name)
        avl_times['delete'].append(time.time() - start)

        # RBT
        rbt = RedBlackTree()
        start = time.time()
        for i in range(n): rbt.insert(names[i], phones[i])
        rbt_times['insert'].append(time.time() - start)
        start = time.time()
        for name in search_names: rbt.search(name)
        rbt_times['search'].append(time.time() - start)
        start = time.time()
        for name in delete_names: rbt.delete(name)
        rbt_times['delete'].append(time.time() - start)

    # Plot
    plt.figure(figsize=(14, 10))

    plt.subplot(3, 1, 1)
    plt.plot(sizes, bst_times['insert'], label='BST Insert', marker='o')
    plt.plot(sizes, avl_times['insert'], label='AVL Insert', marker='s')
    plt.plot(sizes, rbt_times['insert'], label='RBT Insert', marker='^')
    plt.ylabel('Time (seconds)')
    plt.title('Insertion Time vs Input Size (BST vs AVL vs Red-Black Tree)')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(sizes, bst_times['search'], label='BST Search', marker='o')
    plt.plot(sizes, avl_times['search'], label='AVL Search', marker='s')
    plt.plot(sizes, rbt_times['search'], label='RBT Search', marker='^')
    plt.ylabel('Time (seconds)')
    plt.title('Search Time vs Input Size (BST vs AVL vs Red-Black Tree)')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(sizes, bst_times['delete'], label='BST Delete', marker='o')
    plt.plot(sizes, avl_times['delete'], label='AVL Delete', marker='s')
    plt.plot(sizes, rbt_times['delete'], label='RBT Delete', marker='^')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Time (seconds)')
    plt.title('Deletion Time vs Input Size (BST vs AVL vs Red-Black Tree)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ===== Combined Benchmark GUI (BST + AVL + RBT) =====

class CombinedBenchmarkApp:
    def __init__(self, master):
        self.master = master
        master.title("BST vs AVL vs Red-Black Tree Benchmark")

        tk.Label(master, text="Run Benchmark Comparing BST, AVL, and Red-Black Tree",
                 font=("Arial", 12, "bold")).pack(pady=5)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Run Benchmark (N=1000)", command=lambda: self.run(1000)).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Run Benchmark (N=5000)", command=lambda: self.run(5000)).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Plot Multi-Size Comparison", command=self.run_multi_size).grid(row=0, column=2, padx=5)

        self.result_text = tk.Text(master, height=12, width=65)
        self.result_text.pack(pady=10)

        self.treeview = ttk.Treeview(master, columns=("Operation", "BST", "AVL", "RBT"), show='headings')
        self.treeview.heading("Operation", text="Operation")
        self.treeview.heading("BST", text="BST Time (s)")
        self.treeview.heading("AVL", text="AVL Time (s)")
        self.treeview.heading("RBT", text="RBT Time (s)")
        self.treeview.pack(pady=10)

    def run(self, n):
        self.result_text.delete(1.0, tk.END)
        results = benchmark_three_trees(n=n, verbose=False)

        bst = results['BST']
        avl = results['AVL']
        rbt = results['RBT']

        summary = (
            f"Benchmark Results (N={n}):\n"
            f"{'Operation':<12} {'BST':>12} {'AVL':>12} {'RBT':>12}\n"
            f"{'-'*50}\n"
            f"{'Insert':<12} {bst['insert']:>12.6f} {avl['insert']:>12.6f} {rbt['insert']:>12.6f}\n"
            f"{'Search':<12} {bst['search']:>12.6f} {avl['search']:>12.6f} {rbt['search']:>12.6f}\n"
            f"{'Delete':<12} {bst['delete']:>12.6f} {avl['delete']:>12.6f} {rbt['delete']:>12.6f}\n"
            f"\nFound in search: BST={bst['found']}, AVL={avl['found']}, RBT={rbt['found']}\n"
        )
        self.result_text.insert(tk.END, summary)

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        for op_key, label in [('insert', 'Insert'), ('search', 'Search'), ('delete', 'Delete')]:
            self.treeview.insert('', tk.END, values=(
                label,
                f"{results['BST'][op_key]:.6f}",
                f"{results['AVL'][op_key]:.6f}",
                f"{results['RBT'][op_key]:.6f}"
            ))

    def run_multi_size(self):
        sizes = [500, 1000, 2000, 4000, 6000, 8000, 10000]
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Running multi-size benchmark... (this may take a moment)\n")
        self.master.update()
        benchmark_three_trees_for_sizes(sizes)


# ===== Entry Point =====

if __name__ == "__main__":
    import sys

    print("=== Red-Black Tree Contact Directory ===")
    print("Choose mode:")
    print("  1. Open RBT Contact Directory GUI")
    print("  2. Open Combined Benchmark GUI (BST vs AVL vs RBT)")
    print("  3. Run console benchmark only")

    mode = input("Enter 1, 2, or 3 (default=2): ").strip() or "2"

    if mode == "1":
        root = tk.Tk()
        app = RBTreeApp(root)
        root.mainloop()
    elif mode == "3":
        benchmark_three_trees(n=1000)
        benchmark_three_trees(n=5000)
        sizes = [500, 1000, 2000, 4000, 6000, 8000, 10000]
        benchmark_three_trees_for_sizes(sizes)
    else:
        root = tk.Tk()
        app = CombinedBenchmarkApp(root)
        root.mainloop()