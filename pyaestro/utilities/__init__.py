import functools
from threading import Lock
from types import FunctionType


def synchronize(lock):

    def _synchronize(func):
        def _wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)

        return _wrapper

    return _synchronize


def synchronizedclass(cls):
    '''
    if type(cls) is not object:
        raise TypeError(
            "A class must be used with 'synchronizedclase' decorator! "
            "'{cls.__name__}' is not a class.")
    '''
    lock = Lock()
    init = cls.__init__
    def __init__(self, *args, **kwargs):
        self.__lock__ = lock
        init(self, *args, **kwargs)

    cls.__init__ = init

    for key in cls.__dict__:
        method = cls.__dict__[key]
        if type(method) is FunctionType:
            decorator = synchronize(lock)
            cls.__dict__[key] = decorator(method)