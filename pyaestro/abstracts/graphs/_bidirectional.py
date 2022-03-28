from typing import Hashable

from pyaestro.abstracts.graphs._graph import Graph
from pyaestro.typing import Comparable


class BidirectionalGraph(Graph):
    def add_edge(self, a: Hashable, b: Hashable, weight: Comparable = 0):
        """Add an undirected edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
            weight(Comparable): Weight of the edge between 'a' and 'b'.
            Defaults to 0 for unweighted.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        super().add_edge(a, b, weight)
        super().add_edge(b, a, weight)

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove the bidirectional edge from nodes 'a' to 'b' from the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        if a != b:
            super().remove_edge(b, a)
        super().remove_edge(a, b)
