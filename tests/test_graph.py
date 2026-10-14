import graph
import unittest

class GraphTest(unittest.TestCase):

    def setUp(self):
        self.edges = set([
            (0,4),
            (2,3),
            (1,0),
            (5,1),
            (2,5),
            (3,6),
            (6,1),
            (4,1),
            (5,4)
        ])
        
        self.graph = graph.Graph(edge_list = self.edges)
        assert self.graph.edges == self.edges, (self.graph.edges,self.edges)

    def test_update(self):

        self.graph.update(edge_dict = {
            3:[2,8,7],
            6:[7,2],
            8:[7,0]
        })

        edges = set(list(self.edges)+[(3,2),(3,8),(3,7),(6,7),(6,2),(8,7),(8,0)])
        assert self.graph.edges == edges, self.graph.edges

        self.graph.remove(nodes = [5,2], edges = [(6,7), (4,1)])
        edges.difference_update([(6,7),(4,1)])
        to_remove = [e for e in edges if 5 in e or 2 in e]
        edges.difference_update(to_remove)
        assert self.graph.edges == edges, list(zip(sorted(self.graph.edges), sorted(edges)))

        self.graph.remove(nodes = [22], edges = [(15,24)])
        assert self.graph.edges == edges, self.graph.edges

        
        
    def test_eq(self):
        pass

    def test_successor(self):
        pass

if __name__ == '__main__':
    unittest.main()

