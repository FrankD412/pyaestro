from abc import ABC, abstractmethod


class Conductor(ABC):
    @abstractmethod
    def __init__(self, path):
        pass

    @abstractmethod
    def setup_parser():
        pass
