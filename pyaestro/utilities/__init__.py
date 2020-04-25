from functools import wraps
import inspect
from threading import RLock


class SynchronizedClass(type):
    def __new__(cls, name, bases, attrs):
        print(name)
        print(cls)
        lock = RLock()
        _init = cls.__init__
        def __init__(self, *args, **kwargs):
            self.__lock__ = lock
            _init(self, *args, **kwargs)

            for method in inspect.getmembers(cls, inspect.isfunction):
                print("Syncing -- ", method[0])
            decorator = cls.synchronize(self.__lock__)
            setattr(cls, method[0], decorator(getattr(cls, method[0])))

        cls.__init__ = __init__

        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def synchronize(cls, lock):

        def _synchronize(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                with lock:
                    return func(*args, **kwargs)
            return _wrapper
        return _synchronize

"""
def synchronizedclass(cls):
    if not inspect.isclass(cls):
        raise TypeError(
            "A class must be used with 'synchronizedclase' decorator! "
            "'{cls.__name__}' is not a class.")

    lock = Lock()
    init = cls.__init__
    def __init__(self, *args, **kwargs):
        self.__lock__ = lock
        init(self, *args, **kwargs)

    cls.__init__ = init

    for method in inspect.getmembers(cls, inspect.isroutine):
        decorator = synchronize(lock)
        attr = getattr(cls, method[0])
        print(decorator)
        print(attr)
        setattr(cls, method[0], decorator(attr))

    return cls

import types

class DecoMeta(type):
   def __new__(cls, name, bases, attrs):

      for attr_name, attr_value in attrs.iteritems():
         if isinstance(attr_value, types.FunctionType):
            attrs[attr_name] = cls.deco(attr_value)

      return super(DecoMeta, cls).__new__(cls, name, bases, attrs)

   @classmethod
   def deco(cls, func):
      def wrapper(*args, **kwargs):
         print "before",func.func_name
         result = func(*args, **kwargs)
         print "after",func.func_name
         return result
      return wrapper
"""