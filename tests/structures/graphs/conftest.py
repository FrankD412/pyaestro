from math import ceil, sqrt
from random import choices, randint, seed
from typing import Any, Dict, List, Set, Tuple, Type, Union

import pytest
from pytest import FixtureRequest

from pyaestro.abstracts.graphs import Graph
from pyaestro.structures.graphs import BidirectionalAdjGraph
from tests.helpers.utils import generate_unique_upper_names

MAX_WEIGHT = 1000


def pytest_sessionstart(session):
    """Initialize a fixed global random seed for the test session."""
    seed(17)


@pytest.fixture(
    scope="module",
    params=[
        {"malformed": {}, "vertices": {}},
        {"edges": {}, "malformed": {}},
        {"malformed1": {}, "malformed2": {}},
    ],
)
def malformed_specification(request: FixtureRequest) -> Dict[str, Dict]:
    """Creates an invalid specification for a graph data structure.

    Args:
        request (FixtureRequest): Pytest request with test configuration.

    Returns:
        Dict[str, Dict]: Invalid specification.
    """
    return request.param


@pytest.fixture(scope="function")
def valid_specification(
    graph_type: Type[Graph], weighted: bool, sized_node_list: List[str]
) -> Dict[str, Dict[str, Union[List[Tuple[str, Any]], Any]]]:
    """Creates a valid graph specification.

    Args:
        graph_type (Type[Graph]): A Graph class name to test.
        weighted (bool): Enable/Disable weighted test.
        sized_node_list (List[str]): A list of unique node names.

    Returns:
        Dict[str, Dict[str, Union[List[Tuple[str, Any]], Any]]]: A valid
        specification based on the graph_type and sized_node_list.
    """
    spec = {
        "edges": {},
        "vertices": {},
    }
    nodes = sized_node_list
    bidirectional = issubclass(graph_type, BidirectionalAdjGraph)
    _edges = {}

    for node in nodes:
        spec["vertices"][node] = None
        spec["edges"][node] = []
        _edges[node] = {}

    for node in nodes:
        neighbors = choices(nodes, k=randint(1, ceil(sqrt(len(nodes)))))
        for neighbor in neighbors:
            if neighbor in _edges[node]:
                continue

            weight = randint(0, MAX_WEIGHT) if weighted else 0
            _edges[node][neighbor] = weight

            if bidirectional:
                _edges[neighbor][node] = weight

    for node, neighbors in _edges.items():
        spec["edges"][node] = [
            (dest, weight) for dest, weight in neighbors.items()
        ]

    return spec


@pytest.fixture(scope="function", params=[1, 2, 4, 7, 8, 16, 32])
def sized_node_list(request) -> List[str]:
    """Creates a list of unique vertices names.

    Args:
        request (FixtureRequest): Pytest request with test configuration.

    Returns:
        List[str]: A list of unique node names.
    """
    return list(generate_unique_upper_names(request.param))


@pytest.fixture(scope="function", params=[1, 2, 4, 7, 8, 16, 32])
def sized_graph(
    request: FixtureRequest, graph_type: Type[Graph], weighted: bool
) -> Tuple[Graph, Dict[str, Set[str]]]:
    """_summary_

    Args:
        request (FixtureRequest): Pytest request with test configuration.
        graph_type (Type[Graph]): A Graph class name to test.
        weighted (bool): Enable/Disable weighted test.

    Returns:
        Tuple[Graph, Dict[str, Set[str]]]: A constructed graph and a
        dictionary of vertices to a set of neighbors matching the
        contents of the provided graph.
    """
    graph = graph_type()
    bidirectional = issubclass(graph_type, BidirectionalAdjGraph)
    edges = {}
    nodes = list(generate_unique_upper_names(request.param))
    print(nodes)

    for node in nodes:
        graph[node] = None
        edges[node] = {}

    for node in nodes:
        neighbors = choices(nodes, k=randint(1, len(nodes)))

        for neighbor in neighbors:
            if neighbor in edges[node]:
                continue

            weight = randint(0, MAX_WEIGHT) if weighted else 0
            graph.add_edge(node, neighbor, weight)
            edges[node][neighbor] = weight

            if bidirectional:
                edges[neighbor][node] = weight

    _edges = {}
    for node, neighbors in edges.items():
        _edges[node] = set(
            [(key, weight) for key, weight in edges[node].items()]
        )

    print(_edges)
    return graph, _edges


@pytest.fixture(scope="function")
def valid_acyclic_specification(
    weighted: bool, sized_node_list: List[str]
) -> Dict[str, Dict[str, Union[List[Tuple[str, Any]], Any]]]:
    """Generates an acyclic graph specification.

    Args:
        weighted (bool): Enable/Disable weighted test.
        sized_node_list (List[str]): A list of unique node names.

    Returns:
        Dict[str, Dict[str, Union[List[Tuple[str, Any]], Any]]]:
        A valid specification based on sized_node_list that is guaranteed to
        not contain cycles.

    """
    spec = {
        "edges": {},
        "vertices": {},
    }
    nodes = sized_node_list
    _edges = {}

    for node in nodes:
        spec["vertices"][node] = None
        spec["edges"][node] = []
        _edges[node] = {}

    _nodes = [(i, node) for i, node in enumerate(nodes)]
    for i, node in reversed(_nodes):
        if i == 0:
            break
        parent = i // 2
        weight = randint(0, MAX_WEIGHT) if weighted else 0
        _edges[nodes[parent]][node] = weight

    for node, neighbors in _edges.items():
        spec["edges"][node] = [
            (dest, weight) for dest, weight in neighbors.items()
        ]

    return spec


@pytest.fixture(scope="function")
def valid_cyclic_specification(
    weighted: bool, sized_node_list: List[str]
) -> Dict[str, Dict[str, Union[List[Tuple[str, Any]], Any]]]:
    """Generates an cyclic graph specification.

    Args:
        weighted (bool): Enable/Disable weighted test.
        sized_node_list (List[str]): A list of unique node names.

    Returns:
        Dict[str, Dict[str, Union[List[Tuple[str, Any]], Any]]]:
        A valid specification based on sized_node_list that is guaranteed to
        contain at least one cycle.

    """
    spec = {
        "edges": {},
        "vertices": {},
    }
    nodes = sized_node_list
    _edges = {}

    for node in nodes:
        spec["vertices"][node] = None
        spec["edges"][node] = []
        _edges[node] = {}

    _nodes = [(i, node) for i, node in enumerate(nodes)]
    for i, node in reversed(_nodes):
        parent = i // 2
        weight = randint(0, MAX_WEIGHT) if weighted else 0
        _edges[nodes[parent]][node] = weight
        if i == 0:
            break

        weight = randint(0, MAX_WEIGHT) if weighted else 0
        _edges[node][nodes[max(i - 1, 0)]] = weight

    for node, neighbors in _edges.items():
        spec["edges"][node] = [
            (dest, weight) for dest, weight in neighbors.items()
        ]

    return spec
