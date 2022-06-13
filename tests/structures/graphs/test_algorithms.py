import pytest
from typing import List, Type

from pyaestro.abstracts.graphs import Graph
from pyaestro.structures.graphs.algorithms import (
    BreadthFirstSearch,
    DepthFirstSearch,
    GraphSearchProtocol,
)
from pyaestro.structures.graphs import (
    AcyclicAdjGraph,
    AdjacencyGraph,
    BidirectionalAdjGraph,
)

GRAPHS = (AcyclicAdjGraph, AdjacencyGraph, BidirectionalAdjGraph)


@pytest.mark.parametrize("algorithm", (BreadthFirstSearch, DepthFirstSearch))
@pytest.mark.parametrize("graph_type", GRAPHS)
class TestGraphAlgorithms:
    def test_tree_search(
        self, sized_node_list: List[str], algorithm: GraphSearchProtocol,
        graph_type: Type[Graph]
    ) -> None:
        """Tests path searching on a tree-structured graph.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            algorithm (GraphSearchProtocol): Search algorithm run testing on.
            graph_type (Type[Graph]): A Graph class name to test.
        """
        g = graph_type()
        for node in sized_node_list:
            g[node] = None

    def test_linear_search(
        self, sized_node_list: List[str], algorithm: GraphSearchProtocol,
        graph_type: Type[Graph]
    ) -> None:
        """Tests path searching on a linear chain graph.

        Passing condition is that the search returns a path that matches the
        sliding window of the sized_node_list, where each pair of nodes is
        the (node, parent) relationship that the graph search returns.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            algorithm (GraphSearchProtocol): Search algorithm run testing on.
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
        for i, node in enumerate(algorithm.search(g, source)):
            assert node[0] == path[i][0]
            assert node[1] == path[i][1]
            result.append(node)

        assert len(result) == len(path)