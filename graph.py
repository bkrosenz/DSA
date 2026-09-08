from typing import Set, Any, Iterable, Tuple, Dict

class Node:
    children: Set
    
    def __init__(self, value: Any, children: Set[Any] = None): 
        self.children = children if children is not None else set()
        self.value = value

    @property
    def degree(self):
        """get out degree"""
        return len(self.children)
    
    def __hash__(self):
        return hash(self.value)


class Graph:

    def __init__(self, edge_list:Iterable[Tuple[Any,Any]] = None, edge_dict:Dict[Any,Iterable[Any]] = None):
        self.edges = set()
        self.nodes = {}
        
        if edge_list is not None:
            self.update(edge_list = edge_list)
        elif edge_dict is not None:
            self.nodes = dict.fromkeys(edge_dict.keys())
            self.update(edge_dict = edge_dict)

    def update(self, edge_list:Iterable[Tuple[Any,Any]] = None, edge_dict:Dict[Any,Iterable[Any]] = None):
        """add nodes from adjacency list or adjacency dict"""
        if edge_list is not None:
            self.edges.update(edge_list)
            for u,v in edge_list:
                if u not in self.nodes:
                    self.nodes[u] = Node(u)
                self.nodes[u].children.add(v)
        elif edge_dict is not None:
            self.edges.update( (u,v) for u, edges in edge_dict.items() for v in edges )
            for u, edges in edge_dict.items():
                self.nodes[u] = Node(u, set(edges))

    def remove(self, nodes:Iterable = None, edges:Iterable = None):
        """remove a set of nodes with all incoming/outgoing edges, or remove a set of edges (retaining nodes of degree zero).
        Do not raise an error if a node/edge is not found."""
        if edges is not None: 
            for e in edges:
                if e in self.edges:
                    self.edges.remove(e)
                self.nodes[e[0]].remove(e[1])
    
        if nodes is not None: 
            for u in nodes:
                if u in self.nodes:
                    for v in self.nodes[u].children:
                        self.edges.remove((u,v))
                    del self.nodes[u]
    
                    to_remove = set()
                    for e in self.edges:
                        if e[1] == u: # finding incoming edges is O(|E|)
                            to_remove.add(e)
                            self.nodes[e[0]].children.remove(e[1])
                    self.edges.difference_update(to_remove)
    
    def __contains__(self, u: Any):
        return u in self.nodes

    def __getitem__(self, u: Any):
        return self.nodes[u]

    def __len__(self):
        return len(self.nodes)

    def BFS(self, target, order = 'pre'):
        pass

    def DFS(self, target, order = 'pre'):
        pass
    
class UnionFind:
    pass

def kahns_topological_sort(graph: Graph):
    pass


def prims_mst(graph: Graph):
    pass

def kruskals_mst(graph: Graph):
    pass

def dijkstra_shortest_path(graph: Graph, source: Any):
    pass

def bellman_ford_shortest_path(graph: Graph, source: Any):
    pass

def floyd_warshall_shortest_path(graph: Graph):
    pass
