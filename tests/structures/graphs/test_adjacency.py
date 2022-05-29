from itertools import product
from math import ceil
from random import randint, shuffle
from typing import Dict, List, Type

import pytest
from jsonschema import ValidationError

from pyaestro.abstracts.graphs import Graph
from pyaestro.dataclasses import GraphEdge
from pyaestro.structures.graphs import (
    AcyclicAdjGraph,
    AdjacencyGraph,
    BidirectionalAdjGraph,
)
from tests.helpers.utils import generate_unique_lower_names

GRAPHS = (AdjacencyGraph, BidirectionalAdjGraph)


# TODO: Comment each test with more details.


class TestGraphEdge:
    def test_init(self) -> None:
        """Tests the initialization of a new Edge instance."""
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
        """Tests the sort functionality on weighted and unweighted edges."""
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
    def test_repr(self, graph_type: Type[Graph], weighted: bool) -> None:
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
        self,
        graph_type: Type[Graph],
        weighted: bool,
        malformed_specification: Dict,
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
        self,
        graph_type: Type[Graph],
        weighted: bool,
        sized_node_list: List[str],
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
        self,
        graph_type: Type[Graph],
        weighted: bool,
        valid_specification: Dict,
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
            msg = (
                f"'{graph_type.__name__}.from_specification' raised an "
                f"exception. Error: {str(exception)}"
            )
            pytest.fail(msg)

    def test_delitem(
        self,
        graph_type: Type[Graph],
        weighted: bool,
        sized_node_list: List[str],
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
        self,
        graph_type: Type[Graph],
        weighted: bool,
        sized_node_list: List[str],
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
        self, graph_type: Type[Graph], weighted: bool
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
            del graph["missing"]

        assert "not found in graph" in str(excinfo)

    def test_iter(
        self,
        graph_type: Type[Graph],
        weighted: bool,
        sized_node_list: List[str],
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
        self,
        graph_type: Type[Graph],
        weighted: bool,
        sized_node_list: List[str],
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
        self,
        graph_type: Type[Graph],
        weighted: bool,
        sized_node_list: List[str],
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
            graph["missing"]

        assert "not found in graph" in str(excinfo)

        for node in sized_node_list:
            graph[node] = None

        missing = generate_unique_lower_names(len(sized_node_list))
        for node in missing:
            with pytest.raises(KeyError) as excinfo:
                graph[node]

            assert "not found in graph" in str(excinfo)

    def test__setitem__(self, sized_graph: Graph) -> None:
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

    def test__setitem__missing(self, sized_graph: Graph) -> None:
        """Tests that a graph adds an element when missing.

        Passing conditions are being able to set and then access elements of
        a graph instance that do no exist previously.

        Args:
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
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

    @pytest.mark.parametrize("method", ["add_edge", "remove_edge"])
    def test_readonly_edge_ops(self, sized_graph: Graph, method: str) -> None:
        g = sized_graph[0]
        with g as graph:
            g_method = getattr(graph, method)
            with pytest.raises(RuntimeError):
                g_method("A", "B")

    @pytest.mark.parametrize(
        "method, args",
        [
            ("__delitem__", ["A"]),
            ("__setitem__", ["A", None]),
            ("delete_edges", ["A"]),
        ],
    )
    def test_readonly_node_ops(
        self, sized_graph: Graph, method: str, args: List
    ) -> None:
        g = sized_graph[0]
        with g as graph:
            g_method = getattr(graph, method)
            with pytest.raises(RuntimeError):
                g_method(*args)


@pytest.mark.parametrize("graph_type", (AdjacencyGraph, BidirectionalAdjGraph))
@pytest.mark.parametrize("weighted", [True, False])
class TestFullGraphs:
    def test_add_edge(
        self,
        graph_type: Type[Graph],
        weighted: bool,
        valid_specification: Dict,
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
        bidirectional = issubclass(graph_type, BidirectionalAdjGraph)

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
        self, graph_type: Type[Graph], weighted: bool
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
        self, graph_type: Type[Graph], weighted: bool, sized_graph: Graph
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
            edge_set = set(
                [GraphEdge(node, dst, weight) for dst, weight in edges[node]]
            )
            diff = neighbors - edge_set
            assert len(diff) == 0

    def test_get_neighbors_invalid(self, sized_graph: Graph) -> None:
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
        missing_nodes = list(generate_unique_lower_names(num_missing))

        for node in missing_nodes:
            with pytest.raises(KeyError):
                for neighbor in graph.get_neighbors(node):
                    continue

    def test_edges(self, graph_type: Type[Graph], sized_graph: Graph) -> None:
        """Tests that edge retrieval functions against a reference edge set.

        Passing conditions are that a randomly generated graph returns the
        exact edge set when compared against a reference set.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            weighted (bool): Enable/Disable weighted test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        bidirectional = issubclass(graph_type, BidirectionalAdjGraph)

        edges = set()
        for node, edge_set in sized_graph[1].items():
            for e in edge_set:
                edges.add(GraphEdge(node, e[0], e[1]))
                if bidirectional:
                    edges.add(GraphEdge(e[0], node, e[1]))

        diff = set(graph.edges()) - set(edges)
        assert len(diff) == 0

    def test_delete_neighbors(
        self, graph_type: Type[Graph], weighted: bool, sized_graph: Graph
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
        self, graph_type: Type[Graph], weighted: bool, sized_graph: Graph
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
        missing_nodes = list(generate_unique_lower_names(num_missing))
        len_edges = len(list(graph.edges()))

        for key in missing_nodes:
            with pytest.raises(KeyError):
                graph.delete_edges(key)

        assert len(list(graph.edges())) == len_edges

    def test_remove_edge(
        self, graph_type: Type[Graph], sized_graph: Graph
    ) -> None:
        """Tests edge removal per node and per edge.

        Passing conditions are for each node that when an edge is removed
        that connects it to a neighbor that the neighbor no longer appears in
        the node's neighbor listing. This pattern is continued until there are
        no neighbors left for the node. For a bidirectional graph, the reverse
        edge is also tested each time an edge is removed.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        edges = sized_graph[1]
        bidirectional = issubclass(graph_type, BidirectionalAdjGraph)

        for node in edges.keys():
            pruned = list(graph.get_neighbors(node))
            while pruned:
                neighbor = pruned.pop()
                graph.remove_edge(neighbor.source, neighbor.destination)

                assert neighbor not in graph.get_neighbors(node)
                if bidirectional:
                    assert node not in graph.get_neighbors(
                        neighbor.destination
                    )

        assert len(set(graph.edges())) == 0

    def test_remove_edge_missing(
        self, graph_type: Type[Graph], sized_graph: Graph
    ) -> None:
        """Tests edge removal per node for invalid edges.

        Passing conditions are such that for each node a fixed set of invalid
        nodes are generated and a non-existent edge between each node and each
        invalid node are attempted to be removed. Each edge removal should
        raise an exception and after iterating through all nodes the length
        of the edge list should remain unchanged.

        Args:
            graph_type (Type[Graph]): A Graph class name to test.
            sized_graph (Graph): A graph instance populated with nodes.
        """
        graph = sized_graph[0]
        edges = sized_graph[1]
        bidirectional = issubclass(graph_type, BidirectionalAdjGraph)

        num_missing = randint(ceil(len(graph) // 2), len(graph) - 1)
        missing_nodes = list(generate_unique_lower_names(num_missing))
        len_edges = len(list(graph.edges()))

        for node in edges.keys():
            for neighbor in missing_nodes:
                with pytest.raises(KeyError):
                    graph.remove_edge(node, neighbor)
                if bidirectional:
                    with pytest.raises(KeyError):
                        graph.remove_edge(neighbor, node)

        assert len(list(graph.edges())) == len_edges


class TestAcyclicGraph:
    def test_single_node_cycle(self):
        """
        Tests base case of adding a single node cycle for exception.

        This is a base case of a one node cycle that a cycle check should be
        able to detect.

        Passing condition is that an exception is raise when a self-referencing
        edge is created on the single node.
        """
        g = AcyclicAdjGraph()
        g["A"] = None

        with pytest.raises(RuntimeError):
            g.add_edge("A", "A")

    def test_repr(self) -> None:
        """Tests the reproducer (repr) method for Graph classes.

        Passing condition is that  reproducer should always return
        the class name without any parameters.
        """
        ref_repr = "AcyclicAdjGraph(cycle_checker=DefaultCycleCheck)"
        g = AcyclicAdjGraph()
        assert str(g) == ref_repr

    def test_add_nodes(self, sized_node_list: List[str]) -> None:
        """Tests a long chain of nodes with a cycle from last to first.

        Passing condition is that the chain is created with no cycles.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()

        for node in sized_node_list:
            g[node] = None

    def test_multinode_nocycle(self, sized_node_list: List[str]) -> None:
        """
        Tests a multi-node chain to make enforce no cycles.

        A test that simply creates a linear chain with no cycle that will not
        trigger a cycle exception.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()

        if len(sized_node_list) > 1:
            for i in range(1, len(sized_node_list)):
                a = sized_node_list[i - 1]
                b = sized_node_list[i]

                g[a] = None
                g[b] = None

                g.add_edge(a, b)

    def test_multinode_cycle(self, sized_node_list: List[str]) -> None:
        """Tests a multi-node chain with a cycle from last node to the first.

        Creates a single chain of nodes and adds an edge from the the end
        to the start of the chain.

        Passing condition is that an exception is thrown when the last edge is
        added to the graph, forming a cycle.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()
        if len(sized_node_list) > 1:
            for i in range(1, len(sized_node_list)):
                a = sized_node_list[i - 1]
                b = sized_node_list[i]

                g[a] = None
                g[b] = None

                g.add_edge(a, b)

            with pytest.raises(RuntimeError):
                last = len(sized_node_list) - 1
                g.add_edge(sized_node_list[last], sized_node_list[0])

    def test_tree_nocycle(self, sized_node_list: List[str]) -> None:
        """Tests that a tree can be constructed with no exceptions.

        A tree is a structure that has a strictly mono-directional recursive
        structure of a parent to child. Constructing a tree from a list of
        nodes will always fulfill the acyclic property of a DAG (because it is
        a specialized variant of a DAG).

        Passing condition is that given a linearized node list, construct a
        tree using basic indices parent-child calculations. This test should
        not throw an exception throughout the whole construction.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()
        g[sized_node_list[0]] = None

        for i in range(1, len(sized_node_list)):
            g[sized_node_list[i]] = None
            parent = int((i - 1) / 2)
            g.add_edge(sized_node_list[parent], sized_node_list[i])

    def test_tree_nocycle_multiedge(self, sized_node_list: List[str]) -> None:
        """Tests that nodes can have multiple in-edges without exceptions.

        This test starts with a tree structure, which by principle only has a
        parent-child relationship with no edges between branches (guaranteed to
        uphold the acyclic property of an acyclic graph). The test then adds
        edges to the next node in sequence, creating edges between branches but
        maintaining the forward progression of levels always pointing to the
        generation below it (again, upholding acyclic nature as edges are
        always pointed laterally to the node on the right or the first node
        of the next generation).

        Pass condition is that this test can complete without exception.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()
        g[sized_node_list[0]] = None

        for i in range(1, len(sized_node_list)):
            g[sized_node_list[i]] = None
            parent = int((i - 1) / 2)
            g.add_edge(sized_node_list[parent], sized_node_list[i])

        for i in range(1, len(sized_node_list) - 1):
            g.add_edge(sized_node_list[i], sized_node_list[i + 1])

    def test_tree_nocycle_side_edge(self, sized_node_list: List[str]) -> None:
        """Tests that side edges work without exceptions when no cycles present.

        This test starts with a tree structure, which by principle only has a
        parent-child relationship with no edges between branches (guaranteed to
        uphold the acyclic property of an acyclic graph). The test then adds
        edges to the previous node in sequence, creating edges between branches
        but violating the forward progression of generations below it. This
        test guarantees that a cycle will eventually be formed in the layers
        of the graph.

        Pass condition is that this test raises an exception.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()
        g[sized_node_list[0]] = None

        for i in range(1, len(sized_node_list)):
            g[sized_node_list[i]] = None
            parent = int((i - 1) / 2)
            g.add_edge(sized_node_list[parent], sized_node_list[i])

        with pytest.raises(RuntimeError):
            for i in reversed(range(0, len(sized_node_list))):
                parent = max(i - 1, 0)
                g.add_edge(sized_node_list[i], sized_node_list[parent])

    def test_tree_cycle(self, sized_node_list: List[str]) -> None:
        """Tests for cycle detection when adding edges to a parent of a child.

        This test constructs a tree which violates the acyclic property. Once
        the tree is made, we randomly select a node that is not the root and
        attempt to add an edge to its parent forming a cycle which should be
        caught and an exception raised.

        Passing condition is that the tree is able to be constructed and that
        the addition of the last edge from a child to one of its ancestors
        (any node higher in the tree) will cause an exception.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        g = AcyclicAdjGraph()
        g[sized_node_list[0]] = None

        for i in range(1, len(sized_node_list)):
            g[sized_node_list[i]] = None
            parent = int((i - 1) / 2)
            g.add_edge(sized_node_list[parent], sized_node_list[i])

        node = randint(0, len(sized_node_list) - 1)
        parent = max(int((node - 1) / 2), 0)
        with pytest.raises(RuntimeError):
            g.add_edge(sized_node_list[node], sized_node_list[parent])

    @pytest.mark.parametrize("weighted", [True, False])
    def test_tree_nocycle_spec(self, valid_acyclic_specification) -> None:
        """Tests for cycle detection when loading a graph specification.

        This test constructs a tree from a fixed specification that is
        constructed and guaranteed to be a tree. A tree is selected because
        there is no chance of a cycle which should trip no exceptions clauses.

        Passing condition is that the tree is able to be constructed without
        error.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        try:
            AcyclicAdjGraph.from_specification(valid_acyclic_specification)
        except RuntimeError as exception:
            msg = (
                f"'{AcyclicAdjGraph.__name__}.from_specification' "
                f"raised an exception. Error: {str(exception)}"
            )
            pytest.fail(msg)

    @pytest.mark.parametrize("weighted", [True, False])
    def test_tree_cycle_spec(self, valid_cyclic_specification) -> None:
        """Tests for cycle detection when loading a graph specification.

        This test constructs a tree from a fixed specification that is
        constructed and guaranteed to contain a cycle. The base of the graph
        described is a tree with side ways edges added from each descendent
        level to the level about it (at the end of the tree) and therefore
        forming a cycle.

        Passing condition is that the tree raises an exception when parsing
        the specification.

        Args:
            sized_node_list (List[str]): A list of unique node names.
        """
        with pytest.raises(RuntimeError):
            AcyclicAdjGraph.from_specification(valid_cyclic_specification)
