""""""
from abc import ABC, abstractmethod

class MpiAdapter(ABC):
    """An interface for creating MPI enabled commands."""
    def __init__(self):
        pass

    @abstractmethod
    def substitute_cmd(self, cmd, resources):
        pass