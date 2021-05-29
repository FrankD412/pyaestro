import itertools
import pytest
from string import ascii_uppercase
from typing import Type, List


LINEAR = {
    "edges": {
        "A": { "B" },
        "B": { "C" },
        "C": { "D" },
        "D": { "E" },
        "E": {},
    },
    "vertices": {
        "A": None,
        "B": None,
        "C": None,
        "D": None,
        "E": None,
    },
}


@pytest.fixture(params=[2, 4, 8, 16])
def nodes(node_count):
    node_list = []
    for length in itertools.count(1):
        for i in itertools.product(ascii_uppercase, repeat=length):
            node_list.append("".join(i))
        
        if len(node_list) >= node_count:
            return node_list[:node_count]


@pytest.fixture(scope="module")
def linear_graph(nodes) -> List[str]:
    edges = [(v[i-1], v[i]) for i in range(1, len(nodes))]
    return edges

