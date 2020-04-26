from functools import wraps
import inspect
from threading import RLock


class SynchronizedClass(type):

    def __new__(cls, name, bases, namespace, **kwargs):

        sync_cls = super().__new__(cls, name, bases, namespace)
        lock = RLock()

        _init = sync_cls.__init__
        def __init__(self, *args, **kwargs):
            self.__lock__ = lock
            _init(self, *args, **kwargs)

        sync_cls.__init__ = __init__

        print(inspect.getmembers(sync_cls, inspect.isroutine))
        for method in inspect.getmembers(sync_cls, inspect.isroutine):
            print("Syncing -- ", method[0])
            sync = cls.synchronize(lock)
            setattr(
                sync_cls, method[0],
                sync(getattr(sync_cls, method[0]))
            )

    @classmethod
    def synchronize(cls, lock):
        def _synchronize(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                with lock:
                    return func(*args, **kwargs)
            return _wrapper
        return _synchronize
