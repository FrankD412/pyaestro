import functools

from pyaestro.structures.graphs.algorithms import (
    CycleCheckProtocol,
    DefaultCycleCheck,
)


def cycle_check(
    cycle_checker: CycleCheckProtocol = DefaultCycleCheck,
) -> CycleCheckProtocol:
    def inner(function: CycleCheckProtocol) -> CycleCheckProtocol:
        @functools.wraps(function)
        def cycle_check_wrapper(*args, **kwargs) -> bool:
            print(function)
            print(args)
            print(kwargs)
            ret_value = function(*args, **kwargs)

            if cycle_checker.detect_cycles(args[0]):
                raise Exception("Cycle detected")

            return ret_value

        return cycle_check_wrapper

    return inner
