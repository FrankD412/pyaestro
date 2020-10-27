""""""
from abc import ABC, abstractclassmethod


class MpiMixIn(ABC):
    """An interface for creating MPI enabled commands."""

    @abstractclassmethod
    def mpi_command(self, resources, cluster_config=None) -> str:
        pass

    @abstractclassmethod
    def rank_variable(cls):
        pass

    @abstractclassmethof
    def remaining_walltime(cls):
        pass