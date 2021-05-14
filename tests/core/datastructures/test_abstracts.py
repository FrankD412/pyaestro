import pytest
from typing import Hashable, Iterable, Tuple

from pyaestro.core.datastructures.abstracts import Graph, AdjacencyGraph


class ConcreteAbstractGraph(Graph):
    def _delete_edges(self, key: Hashable) -> None:
        pass

    def edges(self) -> Iterable[Tuple[Hashable]]:
        pass

    def add_edge(self, a: Hashable, b: Hashable) -> None:
        pass

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        pass
    
    def delete_edges(self, key: Hashable) -> None:
        pass
    
    def get_neighbors(self, node: Hashable) -> Iterable[Hashable]:
        raise StopIteration


@pytest.fixture(scope="function")
def concrete_graph():
    return ConcreteAbstractGraph()


class TestGraph:
    def test_contains(concrete_graph):
        pass
    
    def test_getitem(concrete_graph):
        pass
    
    def test_setitem(concrete_graph):
        pass
    
    def test_delitem(concrete_graph):
        pass
    
    def test_repr(concrete_graph):
        pass
    
    def test_dfs(concrete_graph):
        pass
    
    def test_bfs(concrete_graph):
        pass
