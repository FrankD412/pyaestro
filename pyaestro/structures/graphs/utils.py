import functools

from pyaestro.structures.graphs.algorithms import (
    CycleCheckProtocol,
    DefaultCycleCheck,
)


def cycle_check_on_return(
    cycle_checker: CycleCheckProtocol = DefaultCycleCheck,
) -> CycleCheckProtocol:
    def inner(function: CycleCheckProtocol) -> CycleCheckProtocol:
        @functools.wraps(function)
        def cycle_check_wrapper(*args, **kwargs) -> bool:
            ret_graph = function(*args, **kwargs)

            if cycle_checker.detect_cycles(ret_graph):
                raise RuntimeError("Cycle detected")

            return ret_graph

        return cycle_check_wrapper

    return inner
