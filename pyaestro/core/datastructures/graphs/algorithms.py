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
    visited: Set[Hashable] = set()
    to_visit: deque[Hashable] = deque()

    to_visit.push((source, None))
    visited.add(source)
    while to_visit:
        root, parent = to_visit.popleft()
        for node in graph.get_neighbors(root):
            if node in visited:
                continue

            to_visit.push((node, root))
            visited.add(node)

        yield root, parent
    

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

    to_visit.append((source, None))
    visited.add(source)
    while to_visit:
        root, parent = to_visit.pop()
        for node in graph.get_neighbors(root):
            if node in visited:
                continue

            to_visit.append((node, root))
            visited.add(node)

        yield root, parent