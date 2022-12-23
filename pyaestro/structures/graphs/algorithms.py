from collections import deque
from typing import Hashable, Iterable, List, Set, Tuple

from pyaestro.abstracts.graphs import Graph


def breadth_first_search(
    graph: Graph, source: Hashable
) -> Iterable[Tuple[Hashable, Hashable]]:
    """Perform a breadth-first search on a graph data structure.

    Args:
        graph (Graph): An instance of a Graph data structure.
        src (Hashable): Vertex to start the search from.

    Returns:
        Iterable[Tuple[Hashable]]: Iterable of tuples representing the
        combination of (node, parent) in the BFS search.
    """
    visited: Set[Hashable] = set()
    to_visit: deque = deque()

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
) -> Iterable[Tuple[Hashable, Hashable]]:
    """Perform a depth-first search on a graph data structure.

    Args:
        graph (Graph): An instance of a Graph data structure.
        src (Hashable): Vertex to start the search from.

    Returns:
        Iterable[Tuple[Hashable]]: Iterable of tuples representing the
        combination of (node, parent) in the DFS search.
    """
    visited: Set[Hashable] = set()
    to_visit: deque = deque()

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


def recursive_topological_sort(graph: Graph) -> List[Hashable]:
    """Perform a topological sort recursively on a graph.

    Args:
        graph (Graph): A graph to perform sorting on.

    Raises:
        RuntimeError: Raised when a cycle is detected in provided graph.

    Returns:
        List[Hashable]: A valid topological sorting for the provided graph.
    """
    temp_markers: set[Hashable] = set()
    perm_markers: set[Hashable] = set()
    topo_order: list[Hashable] = []

    def visit(node):
        if node in perm_markers:
            return

        if node in temp_markers:
            raise RuntimeError()

        temp_markers.add(node)

        for neighbor in graph.get_neighbors(node):
            visit(neighbor.destination)

        temp_markers.remove(node)
        perm_markers.add(node)
        topo_order.append(node)

    for node in graph:
        visit(node)

    return topo_order[::-1]


def topological_sort_iterative(graph: Graph) -> List[Hashable]:
    """Perform a topological sort recursively on a graph.

    Args:
        graph (Graph): A graph to perform sorting on.

    Raises:
        RuntimeError: Raised when a cycle is detected in provided graph.

    Returns:
        List[Hashable]: A valid topological sorting for the provided graph.
    """
    perm_mark: Set[Hashable] = set()
    topo_order: List[Hashable] = []

    for node in graph:
        # We have already visited all nodes and there is no more work to
        # do. Return the ordering.
        if len(perm_mark) == len(graph):
            return topo_order

        # We've already permanently visited this node, do nothing with it.
        if node in perm_mark:
            continue

        # Stacks for performing depth-first search
        visit_stack: deque[Hashable] = deque()
        path_stack: deque[Hashable] = deque()
        temp_mark: Set[Hashable] = set()

        # Otherwise we have found a node that we want to explore
        visit_stack.append(node)
        while visit_stack:
            # Pop the latest
            cur_node = visit_stack.pop()

            # If we hit a node that is temporily marked (under consideration)
            # then we have found a cycle
            if cur_node in temp_mark:
                raise RuntimeError()

            # We've already permanently visited this node, do nothing with it.
            if cur_node in perm_mark:
                continue

            # Add a temporary mark to denote that we've visited already
            temp_mark.add(cur_node)
            path_stack.append(cur_node)

            for neighbor in graph.get_neighbors(cur_node):
                visit_stack.append(neighbor.destination)

        while path_stack:
            cur_node = path_stack.pop()
            perm_mark.add(cur_node)
            topo_order.append(cur_node)

        return topo_order[::-1]


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
