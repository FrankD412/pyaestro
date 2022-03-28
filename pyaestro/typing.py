from __future__ import annotations

from typing_extensions import Protocol


class Comparable(Protocol):
    """A class that defines a comparability interface."""

    def __lt__(self, other: Comparable) -> bool:
        ...
