from collections import defaultdict
from enum import Enum
from typing import List, Tuple

from .abstracts import Graph
from .constants import EdgeType, GraphSearchType


class MultiGraph(Graph):

    def __init__(self, edge_type=EdgeType.BIDIRECTIONAL):
        self._vertices = {}
        self._edges = defaultdict(set)
        self._layers = {
            "__default__": edge_type
        }

    def add_layer(self, layer_name, layer_type):
        self._layers[layer_name] = layer_type

    def add_node(self, name:str, value: object = None) -> None:
        self._vertices[name] = value

    def _get_edges(cls, a:str, b:str, edge_type:EdgeType) -> List[Tuple[str]]:
        if edge_type == EdgeType.BIDIRECTIONAL:
            return [(a, b), (b, a)]

        reverse_edge = EdgeType.is_reverse_type(edge_type)
        if reverse_edge:
            return [(b, a)]
        else:
            return [(a, b)]

    def _check_cycles(self, src:str, layer:str = "__default__") -> bool:
        pass

    def add_edge(self, a:str, b:str, layer:str = "__default__") -> None:
        pass

