from typing import Set, Any, Iterable, Tuple, Dict

from graph import Graph

class KnightsTour:
    def __init__(self, size:int):
        # TODO: allow asymmetric nxm boards
        nodes = set((i,j) for i in range(size) for j in range(size))
        edges = []
        self.moves = [(2,1), (1,2), (-2,-1), (-1,-2), (2,-1), (-1,2), (-2,1), (1,-2)]
        for x,y in nodes:
            for dx,dy in self.moves: 
                proposal = (x+dx,y+dy)
                if proposal in nodes: # TODO: we reduce the number of comparisons by making the graph undirected.
                    edges.append( ( (x,y), proposal ) )
        self.board = Graph(edge_list = edges)
        
        self.size = size

    def calculate_tour(self, start:Tuple[int,int] = (0,0)):
        """Return open knight's tour starting at start position.
        Return None if no tour is possible."""
        if len(self.board) < 5:
            return None
        
        if start not in self.board:
            raise ValueError(f'start node {start} out of bounds')

        tour = [None] * len(self.board)

        for i in range(len(self.board) - 1):
            tour[i] = start
            if not self.board[start].children:
                return None
            next_pos = min(self.board[start].children, key = lambda u: self.board[u].degree)
            self.board.remove(nodes = [start])
            start = next_pos
        tour[-1] = start
        return tour
    
    
if __name__=="__main__":
    for board_size in range(10):
        kt = KnightsTour( board_size ) 
        tour = kt.calculate_tour()
        print(f'{board_size}x{board_size}, tour: {tour}')
