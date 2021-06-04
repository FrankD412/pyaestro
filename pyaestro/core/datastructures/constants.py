from __future__ import annotations
from enum import Enum
from typing import List, Set, Union


class EdgeProperty(Enum):
    ACYCLIC = 0
    FORWARD = 1
    BACKWARD = 2
    BIDIRECTION = 3
    WEIGHTED = 4

    @classmethod
    def reconile_properties(
        cls, properties: Union[List[EdgeProperty], Set[EdgeProperty]]
    ) -> Set[EdgeProperty]:
        """[summary]

        Args:
            properties (Union[List[EdgeProperty], Set[EdgeProperty]]):

        Returns:
            Set[EdgeProperty]: [description]
        """
        ...
