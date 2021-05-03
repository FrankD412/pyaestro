from typing import Hashable, Iterable, Tuple

from ..abstracts import AdjacencyGraph


class DirectedGraph(AdjacencyGraph):
    def __init__(self):
        super().__init__()
        
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        """Add a directed edge from node 'a' to node 'b' to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        self._adj_table[a].add(b)
        
    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove a directed edge from node 'a' to node 'b' to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        self._adj_table[a].remove(b)
        
    def __iter__(self):
        pass
