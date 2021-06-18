import pytest
import random

from pyaestro.core.datastructures.graphs import AdjacencyGraph


@pytest.fixture(scope="function",
                params=["sized_node_list"])
def sized_adj_graph(request):
    graph = AdjacencyGraph()
    edges = {}
    nodes = request.param
    for node in nodes:
        graph[node] = None

    for node in nodes:
        neighbors = random.choices(
            nodes, k=random.randint(1, len(nodes))
        )
        edges[node] = set(neighbors)
        for neighbor in neighbors:
            graph.add_edge(node, neighbor)
            
    return graph