"""A module dedicated to utility metaclasses."""

from functools import wraps
import inspect
from threading import RLock


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


class SynchronizedClass(type):

    def __new__(cls, name, bases, namespace, **kwargs):

        sync_cls = super().__new__(cls, name, bases, namespace)
        lock = RLock()

        _init = sync_cls.__init__

        def __init__(self, *args, **kwargs):
            self.__lock__ = lock
            _init(self, *args, **kwargs)

        sync_cls.__init__ = __init__

        for method in inspect.getmembers(sync_cls, inspect.isroutine):
            sync = cls.synchronize(lock)
            setattr(
                sync_cls, method[0],
                sync(getattr(sync_cls, method[0]))
            )

        return sync_cls

    @classmethod
    def synchronize(cls, lock):
        def _synchronize(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                with lock:
                    return func(*args, **kwargs)
            return _wrapper
        return _synchronize
