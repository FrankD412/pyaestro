from __future__ import annotations
from typing import Dict, Hashable, Type

from . import AdjacencyGraph
from ..abstracts import Graph
from .algorithms import detect_cycles


class DirectedAdjGraph(AdjacencyGraph):
    """A directed variant of the AdjacencyGraph data structure."""
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        """Add a directed edge from node 'a' to node 'b' to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        try:
            # Add each edge
            self._adj_table[a].add(b)
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
            self._adj_table[a].remove(b)
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def delete_edges(self, key: Hashable) -> None:
        self._adj_table[key].clear()


class DirectedAcyclicAdjGraph(DirectedAdjGraph):
    """A directed acyclic variant of the AdjacencyGraph data structure."""

    def _cycle_check(function):
        def cycle_check_wrapper(*args, **kwargs):
            ret_value = function(*args, **kwargs)
            if detect_cycles(args[0]):
                raise Exception("Cycle detected")
            return ret_value
        return cycle_check_wrapper

    @_cycle_check
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        super().add_edge(a, b)
        
    @_cycle_check
    @classmethod
    def from_specification(
        cls,
        specification: Dict[Hashable, Dict[Hashable, object]]
    ) -> Type[Graph]:
        return super().from_specification(specification)