from typing import Any

class Node:
    def __init__(self, value: Any, left: Node | None, right: Node | None, parent: Node | None):
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right

class BinaryTree:
    root: Node
    def __init__(self):
        self.root = Node(None, None)
       
    def BFS(self, val: Any):
        return self.BFS_recursive(val, self.root)

    def BFS_recursive(self, val, node: Node):
        if node is None: node = self.root
        if node.value == val:
            return node
        left = self.BFS_recursive(node.left)
        if left is not None:
            return left
        right = self.BFS_recursive(node.right)
        if right is not None:
            return right
            

class BinarySearchTree:
    root: Node
    def __init__(self):
        self.root = Node(None, None)
       
    def search(self, val: Any, node: Node | str = 'root'):
        if node == 'root': node = self.root
        if node is None:
            return None
        if node.value == val:
            return node
        elif node.value < val:
            return self.search(val, node.left)
        return self.search(val, node.right)
    
    def insert(self, val: Any):
        """Inserts a new node with value val as a leaf"""
        new_node = Node(val, None)
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if val < node.value:
                node = node.left
            else:
                node = node.right
        new_node.parent = parent
        if parent.val is None: 
            self.root = new_node
        elif val < parent.val:
            parent.left = new_node
        else:
            parent.right = new_node
    
    def max(self, node: Node):
        while node.right is not None:
            node = node.right
        return node

    def min(self, node: Node):
        while node.left is not None:
            node = node.left
        return node

    def sucessor(self, node: Node):
        if node.right is not None:
           return self.min(node.right)
        succ = node.parent
        while succ is not None and node == succ.right: # values decrease until we hit a left branch
            node = succ
            succ = succ.parent
        return succ

    def delete(self, node: Node):
        is_left = node.parent.left == node
        if node.left is None: 
            if node.right is None:
                if is_left: 
                     node.parent.left = None
                else:
                     node.parent.right = None
            else:
                if is_left:
                    node.parent.left = node.right 
                else:
                    node.parent.right = node.right 
class BTree:
    pass

class RangeTree(BTree):
    pass

class OrderStatisticTree(BTree):
    pass

class AVLTree(BinaryTree):
    pass

class RedBlackTree(BinaryTree):
    pass
