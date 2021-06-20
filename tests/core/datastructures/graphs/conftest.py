import collections
import itertools
import pytest
import random
from string import ascii_uppercase

from pyaestro.core.datastructures.graphs import AdjacencyGraph


GraphTuple = collections.namedtuple('graph', 'edges')



@pytest.fixture(scope="function",
                params=[1, 2, 4, 7, 8, 16, 32])
def sized_adj_graph(request):
    graph = AdjacencyGraph()
    edges = {}
    size = request.param
    nodes = []

    for length in itertools.count(1):
        for i in itertools.product(ascii_uppercase, repeat=length):
            nodes.append("".join(i))

        if len(nodes) >= size:
            nodes = nodes[:size]
            break

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