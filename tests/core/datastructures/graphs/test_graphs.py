import itertools
import pytest
from jsonschema import ValidationError
import random

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

    def test_delitem(self, sized_node_list):
        graph = AdjacencyGraph()
        values = {}
        for node in sized_node_list:
            values[node] = random.randint(0, 100000)
            graph[node] = values[node]

        random.shuffle(sized_node_list)
        while sized_node_list:
            value = sized_node_list.pop()
            del graph[value]

            assert value not in graph
            assert value not in graph._vertices

    def test_del_missing(self):
        graph = AdjacencyGraph()
        assert len(graph) == 0
        assert len(graph._vertices) == 0

        with pytest.raises(KeyError) as excinfo:
            del graph['missing']

        assert "not found in graph" in str(excinfo)

    def test_add_egde(self, valid_specification):
        graph = AdjacencyGraph()
        for vertex, value in valid_specification["vertices"].items():
            graph[vertex] = value

        for vertex, neighbors in valid_specification["edges"].items():
            for neighbor in neighbors:
                graph.add_edge(vertex, neighbor)

        with pytest.raises(KeyError) as excinfo:
            graph.add_edge("invalid", "A")

        assert "'invalid' not found in graph" in str(excinfo)

        with pytest.raises(KeyError) as excinfo:
            graph.add_edge("A", "invalid")

        assert "'invalid' not found in graph" in str(excinfo)

        with pytest.raises(KeyError) as excinfo:
            graph.add_edge("invalid", "invalid2")

        assert "'invalid' not found in graph" in str(excinfo)

    def test_edges(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]

        for node in edges.keys():
            diff = set(graph.get_neighbors(node)) - edges[node]
            found = [neighbor for neighbor in diff 
                    if node in graph._adj_table[neighbor]]
            found = set(found)
            assert len(found) == len(diff)
            diff = found - diff
            assert len(diff) == 0

    def test_get_edges(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = set()
        for node, edge_set in sized_adj_graph[1].items():
            for e in edge_set:
                edges.add((node, e))
                edges.add((e, node))

        diff = set(graph.edges()) - set(edges)
        assert len(diff) == 0
    
    def test__setitem__(self, sized_adj_graph):
        pass