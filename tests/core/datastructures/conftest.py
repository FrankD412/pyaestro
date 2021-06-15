import itertools
import pytest
from string import ascii_uppercase


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
    node_list = []
    for length in itertools.count(1):
        for i in itertools.product(ascii_uppercase, repeat=length):
            node_list.append("".join(i))

        if len(node_list) >= request.param:
            return node_list[:request.param]
