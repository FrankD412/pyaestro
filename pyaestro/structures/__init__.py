"""A module of different graph types and other properties."""

__all__ = "Singleton"

class Singleton(type):
    """
    A Singleton metaclass for implementing the singleton design pattern.

    Implementation pulled from StackOverflow
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
