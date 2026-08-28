from typing import Any

class Node(object):
    def __init__(self, val: Any, succ: Node, prev: Node = None):
        self.value = val
        self.next = succ
        if prev is not None:
            self.prev = prev

class LinkedList(object):
    head: Node

    def __init__(self):
        self.head = Node(None,None)

        self._length: int = 0

    def append(self, value: Any):
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = Node(value, None)
        self._length += 1

    def __len__(self):
        return self._length

    def __getitem__(self, i: int):
        if i > len(self):
            raise IndexError('list index out of range')
        cur = self.head
        for ix in range(len(self)):
            cur = cur.next
            if ix == i:
                return cur.value

    def remove(self, i: int):
        if i > len(self):
            raise IndexError('list index out of range')
        ix = 0
        cur = self.head
        while cur.next is not None:
            prev, cur = cur, cur.next
            if ix == i:
                self._length -= 1
                prev.next = cur.next
                return
            ix += 1

class DoublyLinkedList(LinkedList):
    pass

class Deque(LinkedList):
    pass

class Stack(LinkedList):
    pass
