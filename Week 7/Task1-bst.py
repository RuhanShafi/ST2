# -------------------------------
# BST Implementation
# -------------------------------


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Traversals
def preorder(root):
    if root:
        print(root.value, end=" ")
        preorder(root.left)
        preorder(root.right)


def inorder(root):
    if root:
        inorder(root.left)
        print(root.value, end=" ")
        inorder(root.right)


def postorder(root):
    if root:
        postorder(root.left)
        postorder(root.right)
        print(root.value, end=" ")


# Count nodes
def count_nodes(root):
    if root is None:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


# Height
def height(root):
    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


# Search
def search_bst(root, val):
    if root is None or root.value == val:
        return root
    if val < root.value:
        return search_bst(root.left, val)
    return search_bst(root.right, val)


# Insert
def insert_bst(root, val):
    if root is None:
        return Node(val)
    if val < root.value:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    return root


# Find minimum
def find_min(root):
    current = root
    while current.left:
        current = current.left
    return current


# Delete
def delete_node(root, val):
    if root is None:
        return root

    if val < root.value:
        root.left = delete_node(root.left, val)
    elif val > root.value:
        root.right = delete_node(root.right, val)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        temp = find_min(root.right)
        root.value = temp.value
        root.right = delete_node(root.right, temp.value)

    return root


# Level order traversal
from collections import deque


def level_order(root):
    if not root:
        return
    queue = deque([root])
    while queue:
        node = queue.popleft()
        print(node.value, end=" ")
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


# -------------------------------
# Contact Directory (BST)
# -------------------------------


class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.left = None
        self.right = None


class ContactDirectory:
    def __init__(self):
        self.root = None

    def insert(self, root, name, phone):
        if root is None:
            return Contact(name, phone)
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
        while root.left:
            root = root.left
        return root

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
            root.name, root.phone = temp.name, temp.phone
            root.right = self.delete(root.right, temp.name)

        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(f"Name: {root.name}, Phone: {root.phone}")
            self.inorder(root.right)


# Test
if __name__ == "__main__":
    directory = ContactDirectory()

    directory.root = directory.insert(directory.root, "Alice", "123")
    directory.root = directory.insert(directory.root, "Bob", "234")
    directory.root = directory.insert(directory.root, "Eve", "345")

    print("All contacts:")
    directory.inorder(directory.root)

    print("\nSearching for Bob:")
    result = directory.search(directory.root, "Bob")
    if result:
        print(result.name, result.phone)

    print("\nDeleting Alice:")
    directory.root = directory.delete(directory.root, "Alice")
    directory.inorder(directory.root)
