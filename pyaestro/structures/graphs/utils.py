import functools
from typing import Callable


def cycle_check(cycle_func: Callable) -> Callable:
    def inner(function):
        @functools.wraps(function)
        def cycle_check_wrapper(*args, **kwargs):
            ret_value = cycle_func(*args, **kwargs)
            if cycle_func(args[0]):
                raise Exception("Cycle detected")
            return ret_value

        return cycle_check_wrapper

    return inner
