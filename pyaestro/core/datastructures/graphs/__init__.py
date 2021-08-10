import functools
from typing import Dict, Hashable, Type

from pyaestro.core.datastructures.abstracts.graphs import Graph
from .algorithms import detect_cycles
from pyaestro.typing import Comparable


class AcyclicGraph(Graph):
    """An acyclic variant of the Graph abstract class."""

    def _cycle_check(function):
        @functools.wraps(function)
        def cycle_check_wrapper(*args, **kwargs):
            ret_value = function(*args, **kwargs)
            if detect_cycles(args[0]):
                raise Exception("Cycle detected")
            return ret_value
        return cycle_check_wrapper

    @_cycle_check
    def add_edge(
        self, a: Hashable, b: Hashable, weight: Comparable = 0
    ) -> None:
        super().add_edge(a, b)

    @_cycle_check
    @classmethod
    def from_specification(
        cls,
        specification: Dict[Hashable, Dict[Hashable, object]]
    ) -> Type[Graph]:
        return super().from_specification(specification)
