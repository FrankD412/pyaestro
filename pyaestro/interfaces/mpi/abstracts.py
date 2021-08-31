""""""
from abc import ABC, abstractmethod


class MpiAdapter(ABC):
    """An interface for creating MPI enabled commands."""

    @classmethod
    @abstractmethod
    def substitute_cmd(self, cmd, resources):
        raise NotImplementedError
