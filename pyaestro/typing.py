from __future__ import annotations

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class Comparable(Protocol):
    """A class that defines a comparability interface."""

    def __lt__(self, other: Comparable) -> bool:
        ...
