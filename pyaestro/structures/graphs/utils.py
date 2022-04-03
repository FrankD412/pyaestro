import functools
from typing import Callable

from pyaestro.structures.graphs.algorithms import detect_cycles


def cycle_check(cycle_func: Callable = detect_cycles) -> Callable:
    def inner(function):
        @functools.wraps(function)
        def cycle_check_wrapper(*args, **kwargs):
            ret_value = function(*args, **kwargs)
            if cycle_func(args[0]):
                raise Exception("Cycle detected")
            return ret_value

        return cycle_check_wrapper

    return inner
