import pytest
import random

from .helpers.utils import generate_unique_upper_names


@pytest.fixture(scope="session")
def linear_graph():
    return {
        "edges": {
            "A": [["B", 0]],
            "B": [["C", 0]],
            "C": [["D", 0]],
            "D": [["E", 0]],
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
            "A": [("B", 0)],
            "B": [("C", 0), ("D", 0)],
            "C": [("E", 0)],
            "D": [("E", 0)],
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
def sized_unweighted_graph(request, graph_type):
    graph = graph_type()
    edges = {}
    nodes = list(generate_unique_upper_names(request.param))
    print(nodes)

    for node in nodes:
        graph[node] = None
        edges[node] = set()

    for node in nodes:
        neighbors = random.choices(
            nodes, k=random.randint(1, len(nodes))
        )

        for neighbor in neighbors:
            graph.add_edge(node, neighbor)
            edges[node].add((neighbor, 0))
            edges[neighbor].add((node, 0))

    print(edges)
    return graph, edges
