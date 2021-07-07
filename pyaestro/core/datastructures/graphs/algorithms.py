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
    """Perform a depth-first search of the provided Graph.

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


def _detect_cycle(
    graph: Graph, node:Hashable, visited: Set[Hashable], rstack: Set[Hashable]
    ) -> bool:
        """
        Recurse through nodes testing for loops.
        :param v: Name of source vertex to search from.
        :param visited: Set of the nodes we've visited so far.
        :param rstack: Set of nodes currently on the path.
        """
        visited.add(node)
        rstack.add(node)

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                if _detect_cycle(graph, neighbor, visited, rstack):
                    return True
            elif neighbor in rstack:
                return True
        rstack.remove(node)
        return False


def detect_cycles(graph: Graph) -> bool:
    """Detect a cycle in a graph.

    Args:
        graph (Graph): An instance of a Graph data structure.

    Returns:
        bool: Returns True if a cycle is detected, False otherwise.
    """
    visited = set()
    rstack = set()

    for node in graph:
        if node not in visited:
            if _detect_cycle(graph, node, visited, rstack):
                return True
    return False
