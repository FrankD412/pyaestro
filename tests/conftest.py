import itertools
import os
import pytest
import random
from string import ascii_uppercase
import sys

from pyaestro.core.datastructures.graphs import AdjacencyGraph

sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))

import utils

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
    return list(utils.generate_unique_upper_names(request.param))


@pytest.fixture(scope="function",
                params=[1, 2, 4, 7, 8, 16, 32])
def sized_adj_graph(request):
    graph = AdjacencyGraph()
    edges = {}
    nodes = list(utils.generate_unique_upper_names(request.param))

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