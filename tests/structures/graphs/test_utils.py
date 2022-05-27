import pytest
from typing import Type

from pyaestro.abstracts.graphs import Graph
from pyaestro.structures.graphs import AdjacencyGraph, BidirectionalAdjGraph

# from pyaestro.structures.graphs.utils import cycle_check_on_return

GRAPHS = (AdjacencyGraph, BidirectionalAdjGraph)


@pytest.mark.parametrize("graph_type", GRAPHS)
@pytest.mark.parametrize("weighted", [False])
class TestGraphUtils:
    def test_cycle_check(
        self, graph_type: Type[Graph], sized_graph: Graph
    ) -> None:
        pass
