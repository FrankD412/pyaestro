from jsonschema import ValidationError
import pytest
from math import ceil
from random import randint, shuffle

from pyaestro.core.datastructures.graphs import Edge
from pyaestro.core.datastructures.graphs.adjacency import \
    AdjacencyGraph, UndirectedAdjGraph
from tests.core.datastructures.graphs import ConcreteAbstractGraph
import tests.helpers.utils as utils

GRAPHS = (ConcreteAbstractGraph, AdjacencyGraph, UndirectedAdjGraph)


@pytest.mark.parametrize("graph_type", GRAPHS)
class TestBaseGraphInterface:
    def test_repr(self, graph_type):
        graph = graph_type()
        assert str(graph) == f"{graph_type.__name__}()"

    def test_malformed_spec_validation(
        self, graph_type, malformed_specification
    ):
        with pytest.raises(ValidationError) as excinfo:
            graph_type.from_specification(malformed_specification)

        assert "required property" in str(excinfo)

    def test_contains(self, graph_type, sized_node_list):
        graph = graph_type()
        print(f"NODES [{len(sized_node_list)}]: {sized_node_list}")
        for node in sized_node_list:
            graph[node] = None

        shuffle(sized_node_list)
        for node in sized_node_list:
            assert node in graph

    def test_valid_spec_validation(self, graph_type, valid_specification):
        try:
            graph_type.from_specification(valid_specification)
        except Exception as exception:
            msg = f"'{graph_type.__name__}.from_specification' raised an " \
                f"exception. Error: {str(exception)}"
            pytest.fail(msg)

    def test_delitem(self, graph_type, sized_node_list):
        graph = graph_type()
        values = {}
        for node in sized_node_list:
            values[node] = randint(0, 100000)
            graph[node] = values[node]

        shuffle(sized_node_list)
        while sized_node_list:
            value = sized_node_list.pop()
            del graph[value]

            assert value not in graph

    def test_len(self, graph_type, sized_node_list):
        graph = graph_type()
        print(f"NODES [{len(sized_node_list)}]: {sized_node_list}")
        for node in sized_node_list:
            graph[node] = None

        assert len(sized_node_list) == len(graph)

    def test_del_missing(self, graph_type):
        graph = graph_type()
        assert len(graph) == 0
        assert len(graph._vertices) == 0

        with pytest.raises(KeyError) as excinfo:
            del graph['missing']

        assert "not found in graph" in str(excinfo)

    def test_iter(self, graph_type, sized_node_list):
        graph = graph_type()
        values = []
        for key in graph:
            values.append(key)

        assert len(values) == 0

        for key in sized_node_list:
            graph[key] = None

        assert len(graph) == len(sized_node_list)
        for key in graph:
            values.append(key)
        assert sorted(values) == sorted(sized_node_list)

    def test_repr(self, graph_type):
        graph = graph_type()
        assert str(graph) == f"{graph_type.__name__}()"

    def test_getitem(self, graph_type, sized_node_list):
        graph = graph_type()
        print(f"NODES [{len(sized_node_list)}]: {sized_node_list}")
        values = {}
        for node in sized_node_list:
            values[node] = randint(0, 100000)
            graph[node] = values[node]

        shuffle(sized_node_list)
        for node in sized_node_list:
            assert graph[node] == values[node]

    def test_getitem_missing(self, graph_type):
        graph = graph_type()
        assert len(graph) == 0
        assert len(graph._vertices) == 0

        with pytest.raises(KeyError) as excinfo:
            graph['missing']

        assert "not found in graph" in str(excinfo)

    def test__setitem__(self, sized_unweighted_graph):
        graph = sized_unweighted_graph[0]
        edges = sized_unweighted_graph[1]

        for node in graph:
            assert graph[node] is None
            graph[node] = 1
            assert graph[node] == 1

    def test__setitem__missing(self, sized_unweighted_graph):
        graph = sized_unweighted_graph[0]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))
        values = {}

        for node in missing_nodes:
            with pytest.raises(KeyError):
                _ = graph[node]
            value = randint(0, 1000)
            graph[node] = value
            values[node] = value

        for node in values.keys():
            assert graph[node] == values[node]



@pytest.mark.parametrize("graph_type", [UndirectedAdjGraph])
class TestBidirectional:

    def test_add_edge(self, graph_type, valid_specification):
        graph = graph_type()
        edges = set()

        for vertex, value in valid_specification["vertices"].items():
            graph[vertex] = value

        for vertex, neighbors in valid_specification["edges"].items():
            for neighbor, weight in neighbors:
                edges.add(Edge(vertex, neighbor, weight))
                edges.add(Edge(neighbor, vertex, weight))
                graph.add_edge(vertex, neighbor, weight)

        diff = set(graph.edges()) - edges
        assert len(diff) == 0

    def test_add_edge_invalid(self, graph_type):
        graph = graph_type()

        with pytest.raises(KeyError) as excinfo:
            graph.add_edge("invalid", "A")

        assert "'invalid' not found in graph" in str(excinfo)

        with pytest.raises(KeyError) as excinfo:
            graph.add_edge("A", "invalid")

        assert "'A' not found in graph" in str(excinfo)

        with pytest.raises(KeyError) as excinfo:
            graph.add_edge("invalid", "invalid2")

        assert "'invalid' not found in graph" in str(excinfo)

    def test_get_neighbors(self, sized_unweighted_graph):
        graph = sized_unweighted_graph[0]
        edges = sized_unweighted_graph[1]

        for node in graph:
            neighbors = set(graph.get_neighbors(node))
            edge_set = \
                set([Edge(node, dst, weight) for dst, weight in edges[node]])
            diff = neighbors - edge_set
            assert len(diff) == 0

    def test_get_neighbors_invalid(self, sized_unweighted_graph):
        graph = sized_unweighted_graph[0]

        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))

        for node in missing_nodes:
            with pytest.raises(KeyError):
                for neighbor in graph.get_neighbors(node):
                    continue

    def test_edges(self, sized_unweighted_graph):
        graph = sized_unweighted_graph[0]
        edges = set()
        for node, edge_set in sized_unweighted_graph[1].items():
            for e in edge_set:
                edges.add(Edge(node, e[0], e[1]))
                edges.add(Edge(e[0], node, e[1]))

        diff = set(graph.edges()) - set(edges)
        assert len(diff) == 0

'''



    def test_delete_edge_missing(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))
        len_edges = len(list(graph.edges()))

        for node in edges.keys():
            for neighbor in missing_nodes:
                with pytest.raises(KeyError):
                    graph.remove_edge(node, neighbor)
                with pytest.raises(KeyError):
                    graph.remove_edge(neighbor, node)

        assert len(list(graph.edges())) == len_edges

    def test_delete_neighbors(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]

        for node in edges.keys():
            graph.delete_edges(node)
            assert len(set(graph.get_neighbors(node))) == 0

        assert len(set(graph.edges())) == 0

    def test_delete_neighbors_missing(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))
        len_edges = len(list(graph.edges()))

        for key in missing_nodes:
            with pytest.raises(KeyError):
                graph.delete_edges(key)

        assert len(set(graph.edges())) == len_edges

    def test_delete_edge(self, sized_adj_graph):
        graph = sized_adj_graph[0]
        edges = sized_adj_graph[1]

        for node in edges.keys():
            pruned = list(graph.get_neighbors(node))
            while pruned:
                neighbor = pruned.pop()
                graph.remove_edge(node, neighbor)

                assert neighbor not in graph.get_neighbors(node)
                if type(graph) is AdjacencyGraph:
                    assert node not in graph.get_neighbors(neighbor)

        assert len(set(graph.edges())) == 0
'''
