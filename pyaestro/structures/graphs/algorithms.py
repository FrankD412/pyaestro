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
    """Perform a topological sort iteratively on a graph.

    Args:
        graph (Graph): A graph to perform sorting on.

    Raises:
        RuntimeError: Raised when a cycle is detected in provided graph.

    Returns:
        List[Hashable]: A valid topological sorting for the provided graph.
    """

    perm_mark: Set[Hashable] = set()
    temp_mark: Set[Hashable] = set()
    topo_order: List[Hashable] = []
    stack: List[Hashable] = []

    for node in graph:
        # We do not need to consider nodes that
        if node in perm_mark:
            continue

        dfs_stack = [node]
        while dfs_stack:
            v = dfs_stack.pop()

            if v in temp_mark:
                raise RuntimeError()

            if v in perm_mark:
                continue

            temp_mark.add(v)
            children = [n.destination for n in graph.get_neighbors(v)]
            dfs_stack.extend(children)

            while stack:
                peek = set(
                    [n.destination for n in graph.get_neighbors(stack[-1])]
                )
                if v in peek:
                    break

                child = stack.pop()
                topo_order.append(child)
                temp_mark.remove(child)
                perm_mark.add(child)

            stack.append(v)

    return stack + topo_order[::-1]


def topological_sort_iterative(graph: Graph) -> List[Hashable]:
    """Perform a topological sort iteratively on a graph.

    Args:
        graph (Graph): A graph to perform sorting on.

    Raises:
        RuntimeError: Raised when a cycle is detected in provided graph.

    Returns:
        List[Hashable]: A valid topological sorting for the provided graph.
    """
    perm_mark: Set[Hashable] = set()
    temp_mark: Set[Hashable] = set()
    topo_order: List[Hashable] = []
    stack: List[Hashable] = []

    for node in graph:
        if node in perm_mark:
            continue

        dfs_stack = [node]

        while dfs_stack:
            v = dfs_stack.pop()
            if v not in perm_mark:
                perm_mark.add(v)  # no need to append to path any more
                dfs_stack.extend(
                    [n.destination for n in graph.get_neighbors(v)]
                )

                peek = (
                    [n.destination for n in graph.get_neighbors(stack[-1])]
                    if stack
                    else []
                )

                while stack and v not in peek:  # new stuff here!
                    topo_order.append(stack.pop())
                stack.append(v)

    return stack + topo_order[::-1]  # new return value!


def iterative_topological_sort(graph, start):
    seen = set()
    stack = []  # path variable is gone, stack and order are new
    order = []  # order will be in reverse order at first
    q = [start]
    while q:
        v = q.pop()
        if v not in seen:
            seen.add(v)  # no need to append to path any more
            q.extend(graph[v])

            while stack and v not in graph[stack[-1]]:  # new stuff here!
                order.append(stack.pop())
            stack.append(v)

    return stack + order[::-1]  # new return value!


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
