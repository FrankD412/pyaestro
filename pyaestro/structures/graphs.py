from collections import defaultdict
from enum import Enum

from pyaestro.abstracts.graphs import Graph


class EdgeType(Enum):
    BIDIRECTIONAL = 0
    FORWARD_DIRECTIONAL = 1
    REVERSE_DIRECTIONAL = 2


class MultiGraph(Graph):
    def __init__(self, edge_type=EdgeType.BIDIRECTIONAL):
        self._vertices = {}
        self._edges = defaultdict(defaultdict(list))
        self._layers = {
            "__default__": edge_type
        }

    def add_layer(self, layer_name, layer_type):
        self._layers[layer_name] = layer_type

    def add_vertex(self, vertex, value=None, layer="__default__"):
        self._vertices[layer][vertex].append(value)

    def add_edge(self, a, b, layer="__default__"):
        layer_type = self._layers[layer]
