from typing import Any

class Node(object):
    def __init__(self, val: Any, succ: Node, prev: Node = None):
        self.value = val
        self.next = succ
        self.prev = prev

    def __repr__(self):
        return f'val: {self.value}, next: {self.next}, prev: {self.prev}'

class LinkedList(object):
    head: Node

    def __init__(self):
        self.head = Node(None, None)

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

    def __iter__(self):
        cur = self.head.next
        # TODO handle empty list
        while cur is not None:
            yield cur
            cur = cur.next


    def __repr__(self):
        return ','.join(v.value for v in self)

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
    def __init__(self):
        super().__init__()
        self.head = Node(None, None, None)
        # TODO make head node special to prevent infinite loops even when head and prev are not none

    def append(self, value: Any):
        new_node = Node(value, None, None)
        prev = self.head.prev if len(self) else self.head
        prev.next = new_node 
        new_node.next = self.head 
        self._length += 1

    def __getitem__(self, i: int):
        if i > len(self):
            raise IndexError('list index out of range')
        cur = self.head
        if i < len(self) // 2:
            for ix in range(len(self)):
                cur = cur.next
                if ix == i:
                    return cur.value
        else:
            for ix in range(len(self), 0, -1):
                cur = cur.prev
                if ix == i:
                    return cur.value

class Deque(DoublyLinkedList):
    def appendleft(self, value: Any):
        new_node = Node(value, None, None)
        new_node.next = self.head.next
        self.head.next = new_node
        new_node.prev = self.head
        new_node.next.prev = new_node
        self._length += 1

    def popleft(self, value: Any):
        cur = self.head.next
        self.head.next = cur.next
        self._length -= 1
        return cur

class Stack(DoublyLinkedList):
    def pop(self, value: Any):
        cur = head.prev
        head.prev = cur.prev
        cur.prev.next = head
        return cur

    def extend(self, values: Iterable):
        for val in values:
            self.append(val)
