import functools
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from pyaestro.abstracts import Singleton


class Executor(metaclass=Singleton):
    def __init__(self, workers):
        self._status_queue = Queue()
        self._thread_pool = ThreadPoolExecutor()

    @staticmethod
    def tracked(func):
        @functools.wraps(func)
        def 