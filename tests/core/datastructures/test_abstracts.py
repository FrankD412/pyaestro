import pytest
from jsonschema import ValidationError
from typing import Hashable, Iterable, Tuple

from pyaestro.core.datastructures.abstracts import Graph


@pytest.fixture(scope="session")
def concrete_graph():
    return ConcreteAbstractGraph()

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

class TestAbstractGraph:
    def test_abstract_instance(self):
        """Tests that the base Graph class cannot be instantiated (abstract).
        """
        with pytest.raises(TypeError) as excinfo:
            Graph()
            
        assert "Can't instantiate abstract class" in str(excinfo)
    
    
    def test_malformed_spec_validation(self, malformed_specificiation):
        with pytest.raises(ValidationError) as excinfo:
            ConcreteAbstractGraph.from_specification(malformed_specificiation)
        
        assert "required property" in str(excinfo)
    
    def test_valid_spec_validation(self, valid_specificiation):
        try:
            ConcreteAbstractGraph.from_specification(valid_specificiation)
        except Exception as exception:
            msg = f"'ConcreteAbstractGraph.from_specification' raised an " \
                f"exception. Error: {str(exception)}"
            pytest.fail(msg)

    def test_len(self, concrete_graph):
        pass
    
    def test_setitem(self, concrete_graph):
        pass
    
    def test_contains(self, concrete_graph):
        pass
    
    def test_getitem(self, concrete_graph):
        pass
    
    def test_delitem(self, concrete_graph):
        pass
    
    def test_repr(self, concrete_graph):
        pass
    