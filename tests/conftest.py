import pytest
import random

from .helpers.utils import generate_unique_upper_names
from pyaestro.core.datastructures.abstracts import BidirectionalGraph

MAX_WEIGHT = 1000


@pytest.fixture(scope="module",
                params=[{"malformed": {}, "vertices": {}},
                        {"edges": {}, "malformed": {}},
                        {"malformed1": {}, "malformed2": {}}])
def malformed_specification(request):
    return request.param


@pytest.fixture(scope="function")
def valid_specification(graph_type, weighted, sized_node_list):
    spec = {
        "edges": {},
        "vertices": {},
    }
    nodes = sized_node_list
    bidirectional = issubclass(graph_type, BidirectionalGraph)
    _edges = {}

    for node in nodes:
        spec["vertices"][node] = None
        spec["edges"][node] = []
        _edges[node] = {}

    for node in nodes:
        neighbors = random.choices(nodes, k=random.randint(1, len(nodes)))
        for neighbor in neighbors:
            if neighbor in _edges[node]:
                continue

            weight = random.randint(0, MAX_WEIGHT) if weighted else 0
            _edges[node][neighbor] = weight

            if bidirectional:
                _edges[neighbor][node] = weight

    for node, neighbors in _edges.items():
        spec["edges"][node] = \
            [(dest, weight) for dest, weight in _edges.items()]

    return spec


@pytest.fixture(scope="function",
                params=[1, 2, 4, 7, 8, 16, 32])
def sized_node_list(request):
    return list(generate_unique_upper_names(request.param))


@pytest.fixture(scope="function",
                params=[1, 2, 4, 7, 8, 16, 32])
def sized_graph(request, graph_type, weighted):
    graph = graph_type()
    bidirectional = issubclass(graph_type, BidirectionalGraph)
    edges = {}
    nodes = list(generate_unique_upper_names(request.param))
    print(nodes)

    for node in nodes:
        graph[node] = None
        edges[node] = {}

    for node in nodes:
        neighbors = random.choices(
            nodes, k=random.randint(1, len(nodes))
        )

        for neighbor in neighbors:
            if neighbor in edges[node]:
                continue

            weight = random.randint(0, MAX_WEIGHT) if weighted else 0
            graph.add_edge(node, neighbor, weight)
            edges[node][neighbor] = weight

            if bidirectional:
                edges[neighbor][node] = weight

    _edges = {}
    for node, neighbors in edges.items():
        _edges[node] = \
            set([(key, weight) for key, weight in edges[node].items()])

    print(_edges)
    return graph, _edges
