from typing import Hashable, Iterable

from pyaestro.typing import Comparable
from . import AcyclicGraph
from ..abstracts import Graph, BidirectionalGraph
from . import Edge


class AdjacencyGraph(Graph):
    """An adjacency list implementation a directed graph."""
    def __init__(self):
        self._adj_table = {}
        super().__init__()

    def __setitem__(self, key: Hashable, value: object) -> None:
        super().__setitem__(key, value)
        if key not in self._adj_table:
            self._adj_table[key] = {}

    def __delitem__(self, key: Hashable) -> None:
        try:
            super().__delitem__(key)
            del self._adj_table[key]
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def edges(self) -> Iterable[Edge]:
        for src, adj_list in self._adj_table.items():
            for dest, weight in adj_list.items():
                yield Edge(src, dest, weight)

    def get_neighbors(self, node: Hashable) -> Iterable[Edge]:
        try:
            for dest, weight in self._adj_table[node].items():
                yield Edge(node, dest, weight)
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

        """A directed variant of the AdjacencyGraph data structure."""

    def add_edge(
        self, a: Hashable, b: Hashable, weight: Comparable = 0
    ) -> None:
        try:
            # Add each edge
            self._adj_table[a][b] = weight
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove a directed edge from node 'a' to node 'b' to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        try:
            del self._adj_table[a][b]
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def delete_edges(self, key: Hashable) -> None:
        try:
            self._adj_table[key].clear()
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")


class BidirectionalAdjGraph(BidirectionalGraph, AdjacencyGraph):
    """An adjacency list implementation a bidirectional graph."""

    def delete_edges(self, key: Hashable) -> None:
        try:
            self._adj_table[key].pop(key, None)
            for neighbor, weight in self._adj_table[key].items():
                del self._adj_table[neighbor][key]
            self._adj_table[key].clear()
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")


class AcyclicAdjGraph(AcyclicGraph, AdjacencyGraph):
    """A directed acyclic variant of the AdjacencyGraph data structure."""
    ...
