from collections import defaultdict
import jsonschema
from typing import Hashable, Iterable, Tuple

from ..abstracts import Graph

class AdjacencyGraph(Graph):
    def __init__(self):
        self._adj_table = defaultdict(set)
        super().__init__()

    def edges(self) -> Iterable[Tuple[Hashable]]:
        for src, adj_list in self._adj_table.items():
            for dest in adj_list: 
                yield src, dest

    def get_neighbors(self, node: Hashable) -> Iterable[Hashable]:
        for dest in self._adj_table[node]:
            yield dest
            
    def delete_edges(self, key: Hashable) -> None:
        for neighbor in self._adj_table[key]:
            self._adj_table[neighbor].remove(key)
        self._adj_table[key].clear()
        
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        """Add an edge between node 'a' and node 'b' to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        self._adj_table[a].add(b)
        self._adj_table[b].add(a)

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove a edge between node 'a' and node 'b' from the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        self._adj_table[a].remove(b)
        self._adj_table[b].remove(a)