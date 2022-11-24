from math import floor, log2
import pytest
from typing import List, Type

from pyaestro.abstracts.graphs import Graph
from pyaestro.structures.graphs.algorithms import (
    breadth_first_search,
    depth_first_search,
)
from pyaestro.structures.graphs import (
    AcyclicAdjGraph,
    AdjacencyGraph,
    BidirectionalAdjGraph,
)

GRAPHS = (AcyclicAdjGraph, AdjacencyGraph, BidirectionalAdjGraph)


@pytest.mark.parametrize("graph_type", GRAPHS)
class TestDepthFirstSearch:
    def test_tree_search(
        self, sized_node_list: List[str], graph_type: Type[Graph]
    ) -> None:
        """Tests path searching on a tree-structured graph.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            graph_type (Type[Graph]): A Graph class name to test.
        """
        g = graph_type()
        g[sized_node_list[0]] = 0

        for i in range(1, len(sized_node_list)):
            g[sized_node_list[i]] = floor(log2(i + 1))
            parent = int((i - 1) / 2)
            g.add_edge(sized_node_list[parent], sized_node_list[i])

        path = list(depth_first_search(g, sized_node_list[0]))
        # In this case, we expect to hit all nodes; lengths must match since
        # all nodes are in path.
        assert len(path) == len(sized_node_list)
        # There is no parent to the root node on the path.
        assert path[0][1] == None

        for node, parent in path[1::]:
            # We expect that the current node in the path to be +1 depth from
            # its parent.
            print(path)
            print(g._vertices)
            assert g[node] == (g[parent] + 1)

    def test_linear_search(
        self, sized_node_list: List[str], graph_type: Type[Graph]
    ) -> None:
        """Tests path searching on a linear chain graph.

        Passing condition is that the search returns a path that matches the
        sliding window of the sized_node_list, where each pair of nodes is
        the (node, parent) relationship that the graph search returns.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            graph_type (Type[Graph]): A Graph class name to test.
        """
        print(sized_node_list)
        path = []
        source = sized_node_list[0]
        g = graph_type()
        g[sized_node_list[0]] = None
        path.append((sized_node_list[0], None))
        for i in range(1, len(sized_node_list)):
            path.append((sized_node_list[i], sized_node_list[i-1]))
            g[sized_node_list[i]] = None
            g.add_edge(sized_node_list[i-1], sized_node_list[i])

        result = []
        for i, node in enumerate(depth_first_search(g, source)):
            assert node[0] == path[i][0]
            assert node[1] == path[i][1]
            result.append(node)

        assert len(result) == len(path)


@pytest.mark.parametrize("graph_type", GRAPHS)
class TestBreadthFirstSearch:
    def test_tree_search(
        self, sized_node_list: List[str], graph_type: Type[Graph]
    ) -> None:
        """Tests path searching on a tree-structured graph.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            graph_type (Type[Graph]): A Graph class name to test.
        """
        g = graph_type()
        g[sized_node_list[0]] = 0
        depths = [0]

        for i in range(1, len(sized_node_list)):
            depths.append(floor(log2(i + 1)))
            g[sized_node_list[i]] = depths[-1]
            parent = int((i - 1) / 2)
            g.add_edge(sized_node_list[parent], sized_node_list[i])

        path = list(breadth_first_search(g, sized_node_list[0]))
        # In this case, we expect to hit all nodes; lengths must match since
        # all nodes are in path.
        assert len(path) == len(sized_node_list)
        # There is no parent to the root node on the path.
        assert path[0][1] == None

        i = 1
        depths.sort()
        for node, parent in path[1::]:
            # We expect that the current node in the path to be +1 depth from
            # its parent.
            print(path)
            print(g._vertices)
            assert g[node] == (g[parent] + 1)
            assert g[node] == depths[i]
            i += 1

    def test_linear_search(
        self, sized_node_list: List[str], graph_type: Type[Graph]
    ) -> None:
        """Tests path searching on a linear chain graph.

        Passing condition is that the search returns a path that matches the
        sliding window of the sized_node_list, where each pair of nodes is
        the (node, parent) relationship that the graph search returns.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            graph_type (Type[Graph]): A Graph class name to test.
        """
        print(sized_node_list)
        path = []
        source = sized_node_list[0]
        g = graph_type()
        g[sized_node_list[0]] = None
        path.append((sized_node_list[0], None))
        for i in range(1, len(sized_node_list)):
            path.append((sized_node_list[i], sized_node_list[i-1]))
            g[sized_node_list[i]] = None
            g.add_edge(sized_node_list[i-1], sized_node_list[i])

        result = []
        for i, node in enumerate(breadth_first_search(g, source)):
            assert node[0] == path[i][0]
            assert node[1] == path[i][1]
            result.append(node)

        assert len(result) == len(path)