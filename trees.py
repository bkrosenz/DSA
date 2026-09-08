from basic import Stack, Deque
from typing import Any, List, Hashable

class TreeNode:
    def __init__(self, value: Any, parent: TreeNode | None, children: List[TreeNode] = None):
        self.value = value
        self.parent = parent
        self.children = [None] * 2 

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    @left.setter
    def left(self, val):
        self.children[0] = val

    @right.setter
    def right(self, val):
        self.children[1] = val

class BinaryTree:
    root: TreeNode
    def __init__(self):
        self.root = TreeNode(None, None)
        self._length = 0
       
    def BFS(self, val: Any):
        return self.BFS_recursive(val, self.root)

    def BFS_recursive(self, val, node: TreeNode):
        if node is None: node = self.root
        if node.value == val:
            return node
        left = self.BFS_recursive(node.left)
        if left is not None:
            return left
        right = self.BFS_recursive(node.right)
        if right is not None:
            return right
            
    def __eq__(self, other):
        sstack, ostack = Stack(), Stack()
        sstack.append(self.root)
        ostack.append(other.root)
        while not sstack.empty and ostack.empty:
            snode, onode = sstack.pop(), ostack.pop()
            if snode is None and onode is not None or onode is None and snode is not None or snode.value != onode.value:
                return False
            sstack.extend(snode.children)
            ostack.extend(onode.children)
        return True

    def __repr__(self):
        dfs = []
        s = Stack()
        s.append(self.root)
        while not s.empty:
            v = s.pop()
            dfs.append(v.value)
            s.extend(v.children)
        return ','.join(map(str, dfs))

class BinarySearchTree(BinaryTree):
       
    def search(self, val: Any, node: TreeNode | str = 'root'):
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
        new_node = TreeNode(val, None)
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if node.value is None or val < node.value:
                node = node.left
            else:
                node = node.right
        new_node.parent = parent
        if parent.value is None: 
            self.root = new_node
        elif val < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node
        self._length += 1
    
    def max(self, node: TreeNode):
        while node.right is not None:
            node = node.right
        return node

    def min(self, node: TreeNode):
        while node.left is not None:
            node = node.left
        return node

    def sucessor(self, node: TreeNode):
        if node.right is not None:
           return self.min(node.right)
        succ = node.parent
        while succ is not None and node == succ.right: # values decrease until we hit a left branch
            node = succ
            succ = succ.parent
        return succ

    def delete(self, node: TreeNode):
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
