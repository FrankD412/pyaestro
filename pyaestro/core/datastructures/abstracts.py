"""A module of different graph types and other properties."""
from __future__ import annotations
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from typing import Hashable, Iterable, Tuple

from .constants import GraphSearchType


class Graph(ABC):
    def __init__(self):
        self._vertices = {}

    def __contains__(self, key) -> bool:
        return self._vertices.__contains__(key)

    def __getitem__(self, key):
        if key not in self._vertices:
            raise KeyError(f"Key '{key}' is not in graph.")

        return self._vertices.get(key)

    def __setitem__(self, key: Hashable, value: object) -> None:
        self._vertices[key] = value

    def __repr__(self) -> str:
        return "{}()".format(type(self).__name__)

    def edges(self) -> Iterable[Tuple[Hashable]]:
        """Iterate the edges of a graph.

        Returns:
            Iterable[Tuple[Hashable]]: An iterable of tuples containing edges.
        """
        ...

    @abstractmethod
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        """Add an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        ...

    @abstractmethod
    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        ...

    def search(
        self, 
        src: Hashable, search_type: GraphSearchType
    ) -> Iterable[str]:
        """Perform a search on the graph from a specified source node.

        Args:
            src (Hashable): Source key to begin search at. 
            search_type (SearchType): The type of search to be performed.

        Returns:
            Iterable[str]: [description]
        """
        visited = set()

        if search_type == GraphSearchType.BREADTH:
            to_visit = []
            pop = to_visit.pop
        elif search_type == GraphSearchType.DEPTH:
            to_visit = deque()
            pop = to_visit.popleft
        else:
            raise ValueError(f"SearchType '{search_type}' not valid.")
        
        to_visit.append(src)
        visited.add(src)
        while to_visit:
            root = pop()
            for node in self.get_neighbors(root):
                if node in visited:
                    continue

                to_visit.append(node)
                yield root

    @abstractmethod
    def get_neighbors(self, node: Hashable) -> Iterable[Hashable]:
        ...

    @abstractmethod
    def __iter__(self) -> Iterable[str]:
        ...


class AdjacencyGraph(Graph):
    def __init__(self):
        self._adj_table = defaultdict(set)
        super().__init__()

    def edges(self) -> Iterable[Tuple[Hashable]]:
        """Iterate the edges of a graph.

        Returns:
            Iterable[Tuple[Hashable]]: An iterable of tuples containing edges.
        """
        for src, adj_list in self._adj_table.items():
            for dest in adj_list: 
                yield (src, dest)

    def get_neighbors(self, node: Hashable) -> Iterable[Hashable]:
        for dest in self._adj_table[node]:
            yield dest