from collections import deque
from typing import Hashable, Iterable, List, Set

from ..abstracts import Graph


def breadth_first_search(graph: Graph, source: Hashable) -> Iterable[Hashable]:
    """Perform a breadth-first search of the provided Graph.

    Args:
        graph (Graph): [description]
        source (Hashable): [description]

    Returns:
        Iterable: [description]
    """
    visited = set()
    to_visit = deque()

    to_visit.push(source)
    visited.add(source)
    while to_visit:
        root = to_visit.pop()
        for node in graph.get_neighbors(root):
            if node in visited:
                continue

            to_visit.push(node)
            yield root
    

def depth_first_search(graph: Graph, source: Hashable) -> Iterable[Hashable]:
    """[summary]

    Args:
        graph (Graph): [description]
        source (Hashable): [description]

    Returns:
        Iterable: [description]
    """
    visited: Set[Hashable] = set()
    to_visit: List[Hashable] = []

    to_visit.append(source)
    visited.add(source)
    while to_visit:
        root: Hashable = to_visit.pop()
        for node in graph.get_neighbors(root):
            if node in visited:
                continue

            to_visit.push(node)
            yield root