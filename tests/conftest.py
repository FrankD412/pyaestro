import pytest
import random

from .helpers.utils import generate_unique_upper_names
from pyaestro.core.datastructures.graphs import AdjacencyGraph
from pyaestro.core.datastructures.graphs.directed import DirectedAdjGraph

import tests.helpers.utils as utils


@pytest.fixture(scope="session")
def linear_graph():
    return {
        "edges": {
            "A": ["B"],
            "B": ["C"],
            "C": ["D"],
            "D": ["E"],
            "E": [],
        },
        "vertices": {
            "A": None,
            "B": None,
            "C": None,
            "D": None,
            "E": None,
        },
    }


@pytest.fixture(scope="session")
def diamond_graph():
    return {
        "edges": {
            "A": ["B"],
            "B": ["C", "D"],
            "C": ["E"],
            "D": ["E"],
            "E": [],
        },
        "vertices": {
            "A": None,
            "B": None,
            "C": None,
            "D": None,
            "E": None,
        },
    }


@pytest.fixture(scope="module",
                params=[AdjacencyGraph, DirectedAdjGraph])
def graph_type(request):
    return request.param


@pytest.fixture(scope="module",
                params=[{"malformed": {}, "vertices": {}},
                        {"edges": {}, "malformed": {}},
                        {"malformed1": {}, "malformed2": {}}])
def malformed_specification(request):
    return request.param


@pytest.fixture(scope="module",
                params=["linear_graph", "diamond_graph"])
def valid_specification(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(scope="function",
                params=[1, 2, 4, 7, 8, 16, 32])
def sized_node_list(request):
    return list(generate_unique_upper_names(request.param))


@pytest.fixture(scope="function",
                params=[1, 2, 4, 7, 8, 16, 32])
def sized_adj_graph(request, graph_type):
    graph = graph_type()
    edges = {}
    nodes = list(generate_unique_upper_names(request.param))

    for node in nodes:
        graph[node] = None
        edges[node] = set()

    for node in nodes:
        neighbors = random.choices(
            nodes, k=random.randint(1, len(nodes))
        )
        
        for neighbor in neighbors:
            graph.add_edge(node, neighbor)
            edges[node].add(neighbor)
            edges[neighbor].add(node)

    return graph, edges