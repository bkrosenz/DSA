import unittest

class BSBTTest(unittest.TestCase):

    def setUp(self):
        self.tree = tree.BinarySearchTree()

        for val in [1, 9, 8, 83, 2, 9, 4, 11, 25, 14]:
            self.tree.insert(val)

    def test_eq():
        pass

    def test_successor():
        pass
    
    def test_insert():
        pass
    
    def test_delete():
        pass
