from __future__ import annotations
from enum import Enum


class EdgeType(Enum):
    BIDIRECTIONAL = "bidirectional"
    FORWARD = "forward"
    REVERSE = "reverse"
    FORWARD_ACYCLIC = "forward acyclic"
    REVERSE_ACYCLIC = "reverse acyclic"

    @staticmethod
    def is_reverse_type(edge_type:EdgeType) -> bool:
        """[summary]

        Args:
            edge_type (EdgeType): [description]

        Returns:
            bool: [description]
        """

        if "reverse" in edge_type.value:
            return True
        return False


class EdgeProperty(Enum):
    FORWARD = 0
    BACKWARD = 1
    


class GraphSearchType(Enum):
    BREADTH = "bfs"
    DEPTH = "dfs"