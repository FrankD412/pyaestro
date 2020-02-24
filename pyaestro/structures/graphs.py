from collections import defaultdict

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