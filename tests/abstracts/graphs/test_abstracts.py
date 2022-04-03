import pytest

from pyaestro.abstracts.graphs import Graph


class TestAbstractGraph:
    def test_abstract_instance(self):
        """Tests that Graph class cannot be instantiated (abstract)."""
        with pytest.raises(TypeError) as excinfo:
            Graph()

        assert "Can't instantiate abstract class" in str(excinfo)
