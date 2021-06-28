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



