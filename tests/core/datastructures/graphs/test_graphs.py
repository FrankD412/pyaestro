import pytest
from jsonschema import ValidationError

from pyaestro.core.datastructures.graphs import AdjacencyGraph


class TestAdjGraph:
    def test_repr(self):
        graph = AdjacencyGraph()
        assert str(graph) == "AdjacencyGraph()"

    def test_malformed_spec_validation(self, malformed_specification):
        with pytest.raises(ValidationError) as excinfo:
            AdjacencyGraph.from_specification(malformed_specification)

        assert "required property" in str(excinfo)

    def test_valid_spec_validation(self, valid_specification):
        try:
            AdjacencyGraph.from_specification(valid_specification)
        except Exception as exception:
            msg = f"'AdjacencyGraph.from_specification' raised an " \
                f"exception. Error: {str(exception)}"
            pytest.fail(msg)

    def test_add_egde(self, valid_specification):
        graph = AdjacencyGraph()
        for vertex, value in valid_specification["vertices"].items():
            graph[vertex] = value

        for vertex, neighbors in valid_specification["edges"].items():
            for neighbor in neighbors:
                graph.add_edge(vertex, neighbor)
