"""A module of different graph types and other properties."""
from abc import ABC
from collections import defaultdict
from enum import Enum


class EdgeType(Enum):
    BIDIRECTIONAL         = 0
    FORWARD_DIRECTIONAL   = 1
    REVERSE_DIRECTIONAL   = 2


class Graph(ABC):
    def __init__(self, edge_type=EdgeType.BIDIRECTIONAL):
        self._vertices = {}
        self._edges = defaultdict(list)

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

    def add_edge(self, a, b):
        pass

    def bfs(self, src):
        pass
    
    def dfs(self, src):
        pass


class MultiGraph(Graph):
    def __init__(self):
        self._vertices = {}
        self._edges = defaultdict(defaultdict(list))
        self._layers = {}

    def add_layer(self, layer, layer_type):
        self._layers[layer] = layer_type

    def add_vertex(self, vertex, value=None, *, layer="__default__"):
        self._vertices[layer][vertex].append(value)

    def add_edge(self, a, b, layer="__default__"):
        layer_type = self._layers[layer]



    