from __future__ import annotations

from abc import abstractmethod
from typing_extensions import Protocol, TypeVar


class ComparableInterface(Protocol):
    """A class that defines a comparability interface."""
    @abstractmethod
    def __lt__(self: Comparable, other: Comparable) -> bool:
        raise NotImplementedError()


Comparable = TypeVar("Comparable", bound=ComparableInterface)
