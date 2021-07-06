from __future__ import annotations
from typing import Hashable

from . import AdjacencyGraph


class DirectedAdjGraph(AdjacencyGraph):

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


class class DirectedAcyclicAdjGraph(DirectedAdjGraph):
    def check_cycles(self) -> bool:
        """Check for cycles in a graph instance.

        Returns:
            bool: True if the graph contains a cycle, False otherwise.
        """
        visited = set()
        rstack = set()
        for v in self.values:
            if v not in visited:
                if self._detect_cycle(v, visited, rstack):
                    return True
                
    def _detect_cycle(self, v, visited, rstack):
        """
        Recurse through nodes testing for loops.
        :param v: Name of source vertex to search from.
        :param visited: Set of the nodes we've visited so far.
        :param rstack: Set of nodes currently on the path.
        """
        visited.add(v)
        rstack.add(v)

        for c in self.adjacency_table[v]:
            if c not in visited:
                if self._detect_cycle(c, visited, rstack):
                    return True
            elif c in rstack:
                return True
        rstack.remove(v)
        return False

    @staticmethod
    def __cycle_check__(func):
    def cycle_wrapper(self, *args, **kwargs):
            ret_value = func(*args, **kwargs)
            if self.check_cycles():
                raise Exception()
            return ret_value

    @DirectedAcyclicAdjGraph.__cycle_check__
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        super.add_edge(a, b)