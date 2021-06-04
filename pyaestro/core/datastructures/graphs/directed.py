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

    def delete_edges(self, key: Hashable) -> None:
        self._adj_table[key].clear()


class DirectedAcyclicAdjGraph(DirectedAdjGraph):
    def check_cycles(self) -> bool:
        """Check for cycles in a graph instance.

        Returns:
            bool: True if the graph contains a cycle, False otherwise.
        """
        return False

    @staticmethod
    def __cycle_check__(func):
        def cycle_wrapper(self, *args, **kwargs):
            ret_value = func(*args, **kwargs)
            if self.check_cycles():
                raise Exception()

            return ret_value
