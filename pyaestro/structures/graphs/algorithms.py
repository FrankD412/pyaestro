from collections import deque
from typing import Callable, Hashable, Iterable, List, Set, Tuple

from pyaestro.abstracts.graphs import Graph


def breadth_first_search(
    graph: Graph, source: Hashable
) -> Iterable[Tuple[Hashable]]:
    """Perform a breadth-first search on a graph data structure.

    Args:
        graph (Graph): An instance of a Graph data structure.
        src (Hashable): Vertex to start the search from.

    Returns:
        Iterable[Tuple[Hashable]]: Iterable of tuples representing the
        combination of (node, parent) in the BFS search.
    """
    visited: Set[Hashable] = set()
    to_visit: deque[Hashable] = deque()

    to_visit.append((source, None))
    visited.add(source)
    while to_visit:
        root, parent = to_visit.popleft()
        for edge in graph.get_neighbors(root):
            node = edge.destination

            if node in visited:
                continue

            to_visit.append((node, root))
            visited.add(node)

        yield root, parent


def depth_first_search(
    graph: Graph, source: Hashable
) -> Iterable[Tuple[Hashable]]:
    """Perform a depth-first search on a graph data structure.

    Args:
        graph (Graph): An instance of a Graph data structure.
        src (Hashable): Vertex to start the search from.

    Returns:
        Iterable[Tuple[Hashable]]: Iterable of tuples representing the
        combination of (node, parent) in the DFS search.
    """
    visited: Set[Hashable] = set()
    to_visit: deque[Hashable] = deque()

    to_visit.append((source, None))
    visited.add(source)
    while to_visit:
        root, parent = to_visit.pop()
        for edge in graph.get_neighbors(root):
            node = edge.destination

            if node in visited:
                continue

            to_visit.append((node, root))
            visited.add(node)

        yield root, parent


def detect_cycles(graph: Graph) -> bool:
    """Detect a cycle in a graph.

    Args:
        graph (Graph): An instance of a Graph data structure.

    Returns:
        bool: Returns True if a cycle is detected, False otherwise.
    """

    def _detect_cycle(
        graph: Graph,
        node: Hashable,
        visited: Set[Hashable],
        rstack: Set[Hashable],
    ) -> bool:
        """Recurse through nodes testing for loops.

        Args:
            graph (Graph): An instance of a Graph data structure.
            node (Hashable): Name of source vertex to search from.
            visited (Set[Hashable]): Set of the nodes we've visited so far.
            rstack(Set[Hashable]): Set of nodes currently on the path.

        Returns:
            bool: Returns True if a cycle is detected, False otherwise.
        """
        visited.add(node)
        rstack.add(node)

        for neighbor in graph.get_neighbors(node):
            child = neighbor.destination
            if child not in visited:
                if _detect_cycle(graph, child, visited, rstack):
                    return True
            elif child in rstack:
                return True
        rstack.remove(node)
        return False

    visited = set()
    rstack = set()

    for node in graph:
        if node not in visited:
            if _detect_cycle(graph, node, visited, rstack):
                return True
    return False
