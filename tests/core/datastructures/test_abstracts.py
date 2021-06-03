import pytest
from typing import Hashable, Iterable, Tuple

from pyaestro.core.datastructures.abstracts import Graph


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


@pytest.fixture(scope="session")
def concrete_graph():
    return ConcreteAbstractGraph()


class TestAbstractGraph:
    def test_abstract_instance(self):
        """Tests that the base Graph class cannot be instantiated (abstract).
        """
        with pytest.raises(TypeError) as excinfo:
            Graph()
            
        assert "Can't instantiate abstract class" in str(excinfo)
    
    def test_len(self, concrete_graph):
        pass
    
    @pytest.mark.parametrize("node", ["A", "B", "C", "D"])
    def test_setitem(self, concrete_graph, node):
        concrete_graph[node] = None
        expected = [node]
        assert len(concrete_graph._vertices) == len(expected)
    
    def test_contains(self, concrete_graph):
        pass
    
    def test_getitem(self, concrete_graph):
        pass
    
    def test_delitem(self, concrete_graph):
        pass
    
    def test_repr(self, concrete_graph):
        pass
    