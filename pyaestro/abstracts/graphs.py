"""A module of different graph types and other properties."""
from abc import ABC, abstractmethod
from enum import Enum


class EdgeType(Enum):
    BIDIRECTIONAL = 0
    FORWARD_DIRECTIONAL = 1
    REVERSE_DIRECTIONAL = 2


class Graph(ABC):

    def __contains__(self, item):
        return self._vertices.__contains__(item)

    def __getitem__(self, key):
        if key not in self._vertices:
            raise KeyError()

        return self._vertices.get(key)

    def __setitem__(self, key, value):
        self._vertices[key] = value

    def __repr__(self):
        return "{}()".format(type(self).__name__)

    @abstractmethod
    def add_edge(self, a, b):
        pass

    @abstractmethod
    def bfs(self, src):
        pass

    @abstractmethod
    def dfs(self, src):
        pass
