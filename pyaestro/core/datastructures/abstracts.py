"""A module of different graph types and other properties."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable

from .graphs import SearchType

class Graph(ABC):

    def __init__(self):
        self._vertices = {}

    def __contains__(self, key) -> bool:
        return self._vertices.__contains__(key)

    def __getitem__(self, key):
        if key not in self._vertices:
            raise KeyError(f"Key '{key}' is not in graph.")

        return self._vertices.get(key)

    def __setitem__(self, key, value):
        self._vertices[key] = value

    def __repr__(self) -> str:
        return "{}()".format(type(self).__name__)

    @abstractmethod
    def add_edge(self, a, b) -> None:
        pass

    def add_node(self, name, item) -> None:
        self._vertices[name] = item

    @abstractmethod
    def _bfs(self, src) -> Iterable[str]:
        pass

    @abstractmethod
    def _dfs(self, src) -> Iterable[str]:
        pass

    @abstractmethod
    def search(self, search_type:SearchType) -> Iterable[str]:
        pass

    @abstractmethod
    def __iter__(self) -> Iterable[str]:
        pass