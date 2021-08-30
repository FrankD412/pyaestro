from __future__ import annotations
from dataclasses import dataclass

from pyaestro.typing import Comparable


@dataclass
class GraphEdge:
    source: str
    destination: str
    value: Comparable = 0

    def __hash__(self):
        return hash(f"{self.source}{self.destination}")

    def __lt__(self, other: GraphEdge):
        if self.value < other.value:
            return True
        return False
