import pytest

from pyaestro.core.datastructures.graphs import AdjacencyGraph


class TestAdjGraph:
    def test_repr(self):
        graph = AdjacencyGraph()
        assert str(graph) == "AdjacencyGraph()"
    
    def test_add_egde(self, valid_specificiation):
        graph = AdjacencyGraph()
        for vertex, value in valid_specificiation["vertices"]:
            graph[vertex] = value
            
        for vertex, neighbor in 