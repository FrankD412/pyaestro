"""A module of data structures and other class important to workflow."""
from multiprocessing import Condition, Lock


class MultiRdr1WrDict(dict):
    def __init__(self, *args, **kwargs):
        self._g_lock = Condition(Lock())
        self._w_wait = False
        self._readers = 0

    def __getitem__(self, key):
        self._g_lock.acquire()
        while self._w_wait:
            self._g_lock.wait()

        self._readers += 1
        self._g_lock.release()

        item = super().__getitem__(key)

        self._g_lock.acquire()
        self._readers -= 1
        if self._readers == 0:
            self._g_lock.notify()
        self._g_lock.release()

        return item

    def __setitem__(self, key, value):
        self._g_lock.acquire()
        self._w_wait = True
        while self._readers > 0:
            self._g_lock.wait()

        super().__setitem__(key, value)

        self._w_wait = False
        self._g_lock.notifyAll()
        self._g_lock.release()


class MultiRdrWtrDict(dict):
    def __init__(self, *args, **kwargs):
        self._g_lock = Condition(Lock())
        self._w_wait = False
        self._readers = 0
        self._writers = 0

    def __getitem__(self, key):
        self._g_lock.acquire()
        while self._w_wait or self._writers > 0:
            self._g_lock.wait()

        self._readers += 1
        self._g_lock.release()

        item = super().__getitem__(key)

        self._g_lock.acquire()
        self._readers -= 1
        if self._readers == 0:
            self._g_lock.notify()
        self._g_lock.release()

        return item

    def __setitem__(self, key, value):
        self._g_lock.acquire()
        self._w_wait = True
        while self._readers > 0:
            self._g_lock.wait()

        super().__setitem__(key, value)

        self._w_wait = False
        self._writers -= 1

        if self._writers == 0:
            self._g_lock.notifyAll()
        self._g_lock.release()
