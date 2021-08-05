import pytest
from jsonschema import ValidationError
import random

from pyaestro.core.datastructures.abstracts import Graph


class TestAbstractGraph:
    def test_abstract_instance(self):
        """Tests that the base Graph class cannot be instantiated (abstract).
        """
        with pytest.raises(TypeError) as excinfo:
            Graph()

        assert "Can't instantiate abstract class" in str(excinfo)
