from typing import Hashable, Iterable, Tuple

from ..abstracts import Graph


class AdjacencyGraph(Graph):
    def __init__(self):
        self._adj_table = {}
        super().__init__()

    def __setitem__(self, key: Hashable, value: object) -> None:
        super().__setitem__(key, value)
        if key not in self._adj_table:
            self._adj_table[key] = set()

    def __delitem__(self, key: Hashable) -> None:
        try:
            super().__delitem__(key)
            del self._adj_table[key]
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

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
        try:
            # Add each edge
            self._adj_table[a].add(b)
            self._adj_table[b].add(a)
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove a edge between node 'a' and node 'b' from the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        try:
            # Add each edge
            self._adj_table[a].remove(b)
            self._adj_table[b].remove(a)
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")
