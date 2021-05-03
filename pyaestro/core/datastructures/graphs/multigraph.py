from collections import defaultdict
from enum import Enum
from typing import List, Tuple

from ..abstracts import Graph
from ..constants import EdgeProperty, GraphSearchType


class MultiGraph(Graph):
    def __init__(self, edge_type=EdgeProperty.BIDIRECTION):
        self._vertices = {}
        self._edges = defaultdict(defaultdict(set))
        self._layers = {"__default__": edge_type}

    def add_layer(self, layer_name, layer_type):
        self._layers[layer_name] = layer_type

    def add_node(self, name: str, value: object = None) -> None:
        self._vertices[name] = value

    def add_edge(self, a: str, b: str, layer: str = "__default__") -> None:
        pass
