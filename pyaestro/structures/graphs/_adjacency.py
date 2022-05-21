from typing import Dict, Hashable, Iterable

from pyaestro.abstracts.graphs import BidirectionalGraphInterface, Graph
from pyaestro.dataclasses import GraphEdge
from pyaestro.structures.graphs.algorithms import (
    CycleCheckProtocol,
    DefaultCycleCheck,
)
from pyaestro.structures.graphs.interfaces import DirectedGraphInterface
from pyaestro.typing import Comparable


class AdjacencyGraph(DirectedGraphInterface, Graph):
    """An adjacency list implementation of a directed graph."""

    def __init__(self):
        self._adj_table = {}
        super().__init__()

    def __setitem__(self, key: Hashable, value: object) -> None:
        print("Inside AdjacencyGraph __setitem__")
        super().__setitem__(key, value)
        if key not in self._adj_table:
            self._adj_table[key] = {}

    def __delitem__(self, key: Hashable) -> None:
        try:
            super().__delitem__(key)
            del self._adj_table[key]
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def edges(self) -> Iterable[GraphEdge]:
        """Iterate the edges of a graph.

        Returns:
            Iterable[GraphEdge]: An iterable of tuples containing edges.
        """
        for src, adj_list in self._adj_table.items():
            for dest, weight in adj_list.items():
                yield GraphEdge(src, dest, weight)

    def get_neighbors(self, node: Hashable) -> Iterable[GraphEdge]:
        """Get the connected neighbors of the specified node.

        Args:
            a (Hashable): Key whose neighbor's should be returned.

        Raises:
            KeyError: Raised when 'key' does not exist in the graph.

        Returns:
            Iterable[GraphEdge]: An iterable of GraphEdge records that
            represent the neighbors of the vertex named 'key'.
        """
        try:
            for dest, weight in self._adj_table[node].items():
                yield GraphEdge(node, dest, weight)
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def add_edge(
        self, a: Hashable, b: Hashable, weight: Comparable = 0
    ) -> None:
        """Add an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
            weight(Comparable): Weight of the edge between 'a' and 'b'.
            Defaults to 0 for unweighted.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """

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
        """Delete all edges associated to a key from the Graph.

        Args:
            key (Hashable): Key to a node whose edges are to be removed.

        Raises:
            KeyError: Raised when either node 'key' or does not exist in the
            graph.
        """
        try:
            self._adj_table[key].clear()
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")


class BidirectionalAdjGraph(BidirectionalGraphInterface, AdjacencyGraph):
    """An adjacency list implementation a bidirectional graph."""

    def delete_edges(self, key: Hashable) -> None:
        """Delete all edges associated to a key from the Graph.

        Args:
            key (Hashable): Key to a node whose edges are to be removed.

        Raises:
            KeyError: Raised when either node 'key' or does not exist in the
            graph.
        """
        try:
            self._adj_table[key].pop(key, None)
            for neighbor, _ in self._adj_table[key].items():
                del self._adj_table[neighbor][key]
            self._adj_table[key].clear()
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")


class AcyclicAdjGraph(AdjacencyGraph):
    """A directed acyclic variant of the AdjacencyGraph data structure."""

    def __init__(self, cycle_checker: CycleCheckProtocol = DefaultCycleCheck):
        super().__init__()
        self._cycle_checker: CycleCheckProtocol = cycle_checker

    def add_edge(
        self, a: Hashable, b: Hashable, weight: Comparable = 0
    ) -> None:
        """Add an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
            weight(Comparable): Weight of the edge between 'a' and 'b'.
            Defaults to 0 for unweighted.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
            RuntimeError: Raised when a cycle is introduced by the addition of
            edge (a, b).
        """
        super().add_edge(a, b, weight)
        if self._cycle_checker.detect_cycles(self):
            raise RuntimeError(f"Addition of edge ({a}, {b}) creates a cycle!")

    def __repr__(self) -> str:
        self_cls = self.__class__
        self_cls = f"{self_cls.__module__}.{self_cls.__qualname__}"
        cycle_cls = self._cycle_checker
        cycle_cls = f"{cycle_cls.__module__}.{cycle_cls.__qualname__}"

        return f"{self_cls}(cycle_checker={cycle_cls})"

    @classmethod
    def from_specification(cls, specification: Dict) -> Graph:
        """Creates an instance of a class from a specification dictionary.

        Args:
            specification (Dict): A specification describing the new instance.

        Returns:
            Specifiable: An instance of the Specifiable class.
        """
        return super().from_specification(specification)
