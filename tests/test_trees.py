import trees
import unittest

class BSBTTest(unittest.TestCase):

    def setUp(self):
        self.tree = trees.BinarySearchTree()

        for val in [1, 9, 8, 83, 2, 9, 4, 11, 25, 14]:
            self.tree.insert(val)
        
    def test_eq(self):
        pass

    def test_successor(self):
        pass
    
    def test_insert(self):
        node = self.tree.insert(5)
        t = str(self.tree)
        self.tree.insert(5)
        assert str(self.tree) == t+',5', (str(self.tree), t)

    
    def test_delete(self):
        t = str(self.tree)
        node = self.tree.insert(12)
        self.tree.delete(node)
        assert str(self.tree) == t, (str(self.tree), t)


if __name__ == '__main__':
    unittest.main()

