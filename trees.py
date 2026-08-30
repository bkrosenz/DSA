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
