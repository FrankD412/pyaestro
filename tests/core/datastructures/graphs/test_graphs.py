from jsonschema import ValidationError
import pytest
from math import ceil
from random import randint, shuffle

from pyaestro.core.datastructures.graphs import AdjacencyGraph
from tests.helpers.utils import generate_unique_lower_names


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
            values[node] = randint(0, 100000)
            graph[node] = values[node]

        shuffle(sized_node_list)
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
        edges = set()
        for vertex, value in valid_specification["vertices"].items():
            graph[vertex] = value

        for vertex, neighbors in valid_specification["edges"].items():
            for neighbor in neighbors:
                edges.add((vertex, neighbor))
                edges.add((neighbor, vertex))
                graph.add_edge(vertex, neighbor)

        diff = set(graph.edges()) - edges
        assert len(diff) == 0

    def test_add_egde_invalid(self, valid_specification):
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

    def test_get_neighbors(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]
        
        for node in graph:
            neighbors = set(graph.get_neighbors(node))
            diff = neighbors - edges[node]
            assert len(diff) == 0

    def test_get_neighbors_invalid(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(generate_unique_lower_names(num_missing))

        for node in missing_nodes:
            with pytest.raises(KeyError):
                for neighbor in graph.get_neighbors(node):
                    continue

    def test_edges(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = set()
        for node, edge_set in sized_adj_graph[1].items():
            for e in edge_set:
                edges.add((node, e))
                edges.add((e, node))

        diff = set(graph.edges()) - set(edges)
        assert len(diff) == 0
    
    def test__setitem__(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]

        for node in graph:
            assert graph[node] == None
            edges_pre = set(graph.get_neighbors(node))
            graph[node] = 1
            edges_post = set(graph.get_neighbors(node))
            assert len(edges_post - edges_pre) == 0
            assert len(edges_post - edges[node]) == 0
            assert graph[node] == 1

    def test__setitem__missing(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(generate_unique_lower_names(num_missing))
        values = {}

        for node in missing_nodes:
            with pytest.raises(KeyError):
                _ = graph[node]
            value = randint(0, 1000)
            graph[node] = value
            values[node] = value

        for node in values.keys():
            assert graph[node] == values[node]

    def test_delete_edge(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(generate_unique_lower_names(num_missing))

        for node in edges.keys():
            pruned = list(graph.get_neighbors(node))
            while pruned:
                neighbor = pruned.pop()
                graph.remove_edge(node, neighbor)

                assert neighbor not in graph.get_neighbors(node)
                assert node not in graph.get_neighbors(neighbor)
                
                for key in missing_nodes:
                    with pytest.raises(KeyError):
                        graph.remove_edge(node, key)
                    with pytest.raises(KeyError):
                        graph.remove_edge(key, node)

        assert len(set(graph.edges())) == 0

    def test_delete_neighbors(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(generate_unique_lower_names(num_missing))

        for key in missing_nodes:
            with pytest.raises(KeyError):
                graph.delete_edges(key)

        for node in edges.keys():
            graph.delete_edges(node)
            assert len(set(graph.get_neighbors(node))) == 0
        
        assert len(set(graph.edges())) == 0

        for key in missing_nodes:
            with pytest.raises(KeyError):
                graph.delete_edges(key)
