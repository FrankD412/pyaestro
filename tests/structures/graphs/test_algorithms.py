import pytest
from typing import List

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
class TestGraphAlgorithms:
    def test_tree_search(
        self, sized_node_list: List[str], algorithm: GraphSearchProtocol
    ) -> None:
        """Tests path searching on a tree-structured graph.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            algorithm (GraphSearchProtocol): Search algorithm run testing on.
        """
        pass

    def test_linear_search(self, sized_node_list: List[str], algorithm: GraphSearchProtocol) -> None:
        """Tests path searching on a linear chain graph.

        Passing condition is that the search returns a path that matches the
        sliding window of the sized_node_list, where each pair of nodes is
        the (node, parent) relationship that the graph search returns.

        Args:
            sized_node_list (List[str]): A list of unique node names.
            algorithm (GraphSearchProtocol): Search algorithm run testing on.
        """
        pass
