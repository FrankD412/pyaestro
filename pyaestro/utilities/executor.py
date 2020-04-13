from concurrent.futures import Thread

from pyaestro.abstracts import Singleton


class Executor(metaclass=Singleton):
    def __init__(self, workers):
        pass