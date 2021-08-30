from itertools import product
from jsonschema import ValidationError
import pytest
from math import ceil
from random import randint, shuffle
from typing import Dict, List, TypeVar, Type

from pyaestro.structures.abstracts import \
    BidirectionalGraph, GraphEdge, Graph
from pyaestro.structures.graphs.adjacency import \
    AdjacencyGraph, BidirectionalAdjGraph
from tests.core.datastructures.graphs import ConcreteAbstractGraph
import tests.helpers.utils as utils

GRAPHS = (ConcreteAbstractGraph, AdjacencyGraph, BidirectionalAdjGraph)
G_TYPE = TypeVar('Graph', bound=Graph)


# TODO: Comment each test with more details.

class TestGraphEdge:
    def test_init(self) -> None:
        """Tests the initialization of a new Edge instance.
        """
        # Unweighted cases
        a = GraphEdge("A", "B", 0)
        b = GraphEdge("A", "B")
        c = GraphEdge("A", "A")
        d = GraphEdge(None, None)

        # Default value/set value should be 0
        assert a.value == 0
        assert b.value == 0
        assert c.value == 0
        assert d.value == 0

        # Weighted Edges
        a = GraphEdge("A", "B", 0)
        b = GraphEdge("A", "B", 1)
        c = GraphEdge("A", "A", 2)
        d = GraphEdge(None, None, 3)

        # Check weights
        assert a.value == 0
        assert b.value == 1
        assert c.value == 2
        assert d.value == 3

    def test_hash(self) -> None:
        """Tests that the hashing for an edge functions.

        Test passes if edges match in hash that have the same source and
        destination. Hashes should not be influenced by an edge's weight.
        """
        a1 = GraphEdge("A", "B", 0)
        b1 = GraphEdge("A", "B")
        c1 = GraphEdge("A", "A")
        d1 = GraphEdge(None, None)

        a2 = GraphEdge("A", "B", 1)
        b2 = GraphEdge("A", "B", 2)
        c2 = GraphEdge("A", "A", 3)
        d2 = GraphEdge(None, None, 4)

        assert hash(a1) == hash(a2)
        assert hash(a1) == hash(b1)
        assert hash(a1) == hash(b2)
        assert hash(b1) == hash(b2)
        assert hash(c1) == hash(c2)
        assert hash(a1) != hash(c1)
        assert hash(d1) == hash(d2)
        assert hash(d1) != hash(c1)

    def test_sort(self, sized_node_list: List[str]) -> None:
        """Tests the sort functionality on weighted and unweighted edges.
        """
        edges = [
            GraphEdge(p[0], p[1], weight)
            for weight, p in enumerate(product(sized_node_list, repeat=2))
        ]
        shuffle(edges)
        edges.sort(reverse=False)

        for i in range(len(edges)):
            assert i == edges[i].value


@pytest.mark.parametrize("graph_type", GRAPHS)
@pytest.mark.parametrize("weighted", [True, False])
class TestBaseGraphInterface:
    def test_repr(self, graph_type: Type[G_TYPE], weighted: bool) -> None:
        """Tests the reproducer (repr) method for Graph classes.

        Passing condition is that a graph's reproducer should always return
        the class name without any parameters.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
        """
        graph = graph_type()
        assert str(graph) == f"{graph_type.__name__}()"

    def test_malformed_spec_validation(
        self, graph_type: Type[G_TYPE], weighted: bool,
        malformed_specification: Dict
    ) -> None:
        """Tests that a Graph class catches malformed specifications.

        Passing condition is that a graph's validation does not allow any
        specification passed to this test to pass.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            malformed_specification (Dict): A malformed graph specification.
        """
        with pytest.raises(ValidationError) as excinfo:
            graph_type.from_specification(malformed_specification)

        assert "required property" in str(excinfo)

    def test_contains(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_node_list: List[str]
    ) -> None:
        """Tests that "in" (__contains__) asserts properly.

        Passing condition is that all nodes can be found in the graph when
        queried at random.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_node_list (List[str]): A list of unique node names.
        """
        graph = graph_type()
        print(f"NODES [{len(sized_node_list)}]: {sized_node_list}")
        for node in sized_node_list:
            graph[node] = None

        shuffle(sized_node_list)
        for node in sized_node_list:
            assert node in graph

    def test_valid_spec_validation(
        self, graph_type: Type[G_TYPE], weighted: bool,
        valid_specification: Dict
    ) -> None:
        """Tests that a Graph class catches malformed specifications.

        Passing condition is that a graph's validation properly constructs
        a graph from the specification passed without any exceptions.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            valid_specification (Dict): A valid graph specification.
        """
        try:
            graph_type.from_specification(valid_specification)
        except Exception as exception:
            msg = f"'{graph_type.__name__}.from_specification' raised an " \
                f"exception. Error: {str(exception)}"
            pytest.fail(msg)

    def test_delitem(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_node_list: List[str]
    ) -> None:
        """Tests the removal of a node from a graph.

        Passing condition is that removal causes the graph to report that it
        no longer contains a node when checked with __contains__(node).

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_node_list (List[str]): A list of unique node names.
        """
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

    def test_len(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_node_list: List[str]
    ) -> None:
        """Tests the length reported by a graph.

        Passing condition is that removal causes the graph to report that it
        no longer contains a node when checked with __contains__(node).

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_node_list (List[str]): A list of unique node names.
        """
        graph = graph_type()
        print(f"NODES [{len(sized_node_list)}]: {sized_node_list}")
        for node in sized_node_list:
            graph[node] = None

        assert len(sized_node_list) == len(graph)

    def test_del_missing(
        self, graph_type: Type[G_TYPE], weighted: bool
    ) -> None:
        """Tests the removal of a missing key from a graph.

        Passing condition is that removal causes the graph to raise an
        exception that notifies of a missing key.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
        """
        graph = graph_type()
        assert len(graph) == 0
        assert len(graph._vertices) == 0

        with pytest.raises(KeyError) as excinfo:
            del graph['missing']

        assert "not found in graph" in str(excinfo)

    def test_iter(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_node_list: List[str]
    ) -> None:
        """Tests the iteration over the nodes in a graph.

        Passing condition is that the proper length is reported by the graph
        when compared to 'sized_node_list' and then all nodes are seen when
        iterating over the graph instance.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_node_list (List[str]): A list of unique node names.
        """
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

    def test_getitem(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_node_list: List[str]
    ) -> None:
        """Tests the indexing [] notation for a graph.

        Passing condition is that a graph with randomly set values for each
        vertex will return the assigned value when indexed to each key.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_node_list (List[str]): A list of unique node names.
        """

        graph = graph_type()
        print(f"NODES [{len(sized_node_list)}]: {sized_node_list}")
        values = {}
        for node in sized_node_list:
            values[node] = randint(0, 100000)
            graph[node] = values[node]

        shuffle(sized_node_list)
        for node in sized_node_list:
            assert graph[node] == values[node]

    def test_getitem_missing(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_node_list: List[str]
    ) -> None:
        """Tests the indexing [] notation for a graph.

        Passing condition is that a graph with randomly set values for each
        vertex will return an exception when accessing a missing key (for both
        an empty and populated graph).

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_node_list (List[str]): A list of unique node names.
        """
        graph = graph_type()
        assert len(graph) == 0
        assert len(graph._vertices) == 0

        with pytest.raises(KeyError) as excinfo:
            graph['missing']

        assert "not found in graph" in str(excinfo)

        for node in sized_node_list:
            graph[node] = None

        missing = utils.generate_unique_lower_names(len(sized_node_list))
        for node in missing:
            with pytest.raises(KeyError) as excinfo:
                graph[node]

            assert "not found in graph" in str(excinfo)

    def test__setitem__(
            self, graph_type: Type[G_TYPE], weighted: bool,
            sized_graph: Graph
    ) -> None:
        """Tests that items can be set using the indexing [] notation.

        Passing conditions are being able to set and then access elements of
        a graph instance.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        values = {}

        for node in graph:
            assert graph[node] is None
            value = randint(0, 1000)
            graph[node] = value
            values[node] = value

        keys = list(values.keys())
        shuffle(keys)
        for key in keys:
            assert graph[key] == values[key]

    def test__setitem__missing(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests that a graph adds an element when missing.

        Passing conditions are being able to set and then access elements of
        a graph instance that do no exist previously.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
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


@pytest.mark.parametrize("graph_type", (AdjacencyGraph, BidirectionalAdjGraph))
@pytest.mark.parametrize("weighted", [True, False])
class TestFullGraphs:

    def test_add_edge(
        self, graph_type: Type[G_TYPE], weighted: bool,
        valid_specification: Dict
    ) -> None:
        """Tests the addition of edges to a graph.

        Passing condition is that graph edges match the specified edges
        in the provided specification.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            valid_specification (Dict): A valid graph specification.
        """
        graph = graph_type()
        edges = set()
        bidirectional = issubclass(graph_type, BidirectionalGraph)

        for vertex, value in valid_specification["vertices"].items():
            graph[vertex] = value

        for vertex, neighbors in valid_specification["edges"].items():
            for neighbor, weight in neighbors:
                edges.add(GraphEdge(vertex, neighbor, weight))
                if bidirectional:
                    edges.add(GraphEdge(neighbor, vertex, weight))
                graph.add_edge(vertex, neighbor, weight)

        diff = set(graph.edges()) - edges
        assert len(diff) == 0

    def test_add_edge_invalid(
        self, graph_type: Type[G_TYPE], weighted: bool
    ) -> None:
        """Tests the addition of edges between non-existent nodes.

        Passing condition is that edges throw an exception when the attempting
        to add edges between at least one invalid nodes.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
        """
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

    def test_get_neighbors(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests neighbor retrieval from a graph instance.

        Passing condition is that the graph returns edges that match a
        reference edge set for a node.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        edges = sized_graph[1]

        for node in graph:
            neighbors = set(graph.get_neighbors(node))
            edge_set = \
                set([GraphEdge(node, dst, weight)
                    for dst, weight in edges[node]])
            diff = neighbors - edge_set
            assert len(diff) == 0

    def test_get_neighbors_invalid(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests exception handling for get_neighbors for invalid nodes.

        Passing conditions are that calling get_neighbors on a node that does
        not exist in the graph raises an exception.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]

        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))

        for node in missing_nodes:
            with pytest.raises(KeyError):
                for neighbor in graph.get_neighbors(node):
                    continue

    def test_edges(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests that edge retrieval functions against a reference edge set.

        Passing conditions are that a randomly generated graph returns the
        exact edge set when compared against a reference set.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        bidirectional = issubclass(graph_type, BidirectionalGraph)

        edges = set()
        for node, edge_set in sized_graph[1].items():
            for e in edge_set:
                edges.add(GraphEdge(node, e[0], e[1]))
                if bidirectional:
                    edges.add(GraphEdge(e[0], node, e[1]))

        diff = set(graph.edges()) - set(edges)
        assert len(diff) == 0

    def test_delete_neighbors(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests exception handling for get_neighbors for invalid nodes.

        Passing conditions are that calling get_neighbors on a node that does
        not exist in the graph raises an exception.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        edges = sized_graph[1]

        for node in edges.keys():
            graph.delete_edges(node)
            assert len(set(graph.get_neighbors(node))) == 0

        assert len(set(graph.edges())) == 0

    def test_delete_neighbors_missing(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests exception handling for get_neighbors for invalid nodes.

        Passing conditions are that calling get_neighbors on a node that does
        not exist in the graph raises an exception.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))
        len_edges = len(list(graph.edges()))

        for key in missing_nodes:
            with pytest.raises(KeyError):
                graph.delete_edges(key)

        assert len(list(graph.edges())) == len_edges

    def test_remove_edge(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests edge removal per node and per edge.

        Passing conditions are for each node that when an edge is removed
        that connects it to a neighbor that the neighbor no longer appears in
        the node's neighbor listing. This pattern is continued until there are
        no neighbors left for the node. For a bidirectional graph, the reverse
        edge is also tested each time an edge is removed.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        edges = sized_graph[1]
        bidirectional = issubclass(graph_type, BidirectionalGraph)

        for node in edges.keys():
            pruned = list(graph.get_neighbors(node))
            while pruned:
                neighbor = pruned.pop()
                graph.remove_edge(neighbor.source, neighbor.destination)

                assert neighbor not in graph.get_neighbors(node)
                if bidirectional:
                    assert \
                        node not in graph.get_neighbors(neighbor.destination)

        assert len(set(graph.edges())) == 0

    def test_remove_edge_missing(
        self, graph_type: Type[G_TYPE], weighted: bool,
        sized_graph: Graph
    ) -> None:
        """Tests edge removal per node for invalid edges.

        Passing conditions are such that for each node a fixed set of invalid
        nodes are generated and a non-existent edge between each node and each
        invalid node are attempted to be removed. Each edge removal should
        raise an exception and after iterating through all nodes the length
        of the edge list should remain unchanged.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        edges = sized_graph[1]
        bidirectional = issubclass(graph_type, BidirectionalGraph)

        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(utils.generate_unique_lower_names(num_missing))
        len_edges = len(list(graph.edges()))

        for node in edges.keys():
            for neighbor in missing_nodes:
                with pytest.raises(KeyError):
                    graph.remove_edge(node, neighbor)
                if bidirectional:
                    with pytest.raises(KeyError):
                        graph.remove_edge(neighbor, node)

        assert len(list(graph.edges())) == len_edges
