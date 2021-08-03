"""A module of different graph types and other properties."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from hashlib import md5
import json
import jsonschema
from os.path import abspath, dirname, join
from typing import Dict, Hashable, Iterable, Tuple, Type

from pyaestro.bases import Specifiable
from pyaestro.typing import Comparable

SCHEMA_DIR = join(dirname(abspath(__file__)), "_schemas")


@dataclass
class Edge:
    source: str
    destination: str
    value: Comparable = 0

    def __hash__(self):
        return hash(f"{self.source}{self.destination}")

    def __lt__(self, other: Edge):
        if self.value < other.value:
            return True
        return False


class Graph(Specifiable, ABC):

    with open(join(SCHEMA_DIR, "graph.json")) as schema:
        _dict_schema = json.load(schema)

    def __init__(self):
        self._vertices = {}

    def __contains__(self, key) -> bool:
        return self._vertices.__contains__(key)

    def __getitem__(self, key):
        try:
            return self._vertices[key]
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def __setitem__(self, key: Hashable, value: object) -> None:
        self._vertices[key] = value

    def __delitem__(self, key: Hashable) -> None:
        try:
            self.delete_edges(key)
            del self._vertices[key]
        except KeyError as key_error:
            raise KeyError(f"Key '{key_error.args[0]}' not found in graph.")

    def __repr__(self) -> str:
        return "{}()".format(type(self).__name__)

    def __iter__(self) -> Iterable[str]:
        for vertex in self._vertices.keys():
            yield vertex

    def __len__(self) -> int:
        return len(self._vertices)

    @classmethod
    def from_specification(
        cls,
        specification: Dict[Hashable, Dict[Hashable, object]]
    ) -> Type[Graph]:
        """Construct a Graph based on a specification of edges and vertices.

        Args:
            specification (Dict[Hashable, Dictionary[Hashable, object]]):
            A dictionary containing two keys:
                - edges: A dictionary of adjacency lists.
                - vertices: A dictionary mapping keys to their values.

        Returns:
            Type[Graph]: An instance of the type Graph.

        Raises:
            ValidationError: Raised when specification does not match the fixed
            schema for a Graph.
        """
        graph = cls()
        jsonschema.validate(
            specification, schema=cls._dict_schema,
            types={'array': (list, tuple)}
        )

        for vertex, value in specification["vertices"].items():
            graph[vertex] = value

        for node, neighbors in specification["edges"].items():
            for neighbor, weight in neighbors:
                graph.add_edge(node, neighbor, weight)

        return graph

    @abstractmethod
    def delete_edges(self, key: Hashable) -> None:
        """Delete all edges associated to a key from the Graph.

        Args:
            key (Hashable): Key to a node whose edges are to be removed.
        """
        raise NotImplementedError

    @abstractmethod
    def edges(self) -> Iterable[Edge]:
        """Iterate the edges of a graph.

        Returns:
            Iterable[Tuple[Hashable]]: An iterable of tuples containing edges.
        """
        raise NotImplementedError

    @abstractmethod
    def add_edge(self, a: Hashable, b: Hashable, weight: Comparable=0) -> None:
        """Add an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
            weight(Comparable): Weight of the edge between 'a' and 'b'.
            Defaults to 0 for unweighted.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        raise NotImplementedError

    @abstractmethod
    def get_neighbors(self, key: Hashable) -> Iterable[Edge]:
        """Get the connected neighbors of the specified node.

        Args:
            a (Hashable): Key whose neighbor's should be returned.

        Raises:
            KeyError: Raised when 'key' does not exist in the graph.

        Returns:
            Iterable[Edge]: An iterable of Edge records that represent the
            neighbors of the vertex named 'key'.
        """
        raise NotImplementedError


class UndirectedGraph(Graph):
    def add_edge(self, a: Hashable, b: Hashable, weight: Comparable = 0):
        """Add an undirected edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
            weight(Comparable): Weight of the edge between 'a' and 'b'.
            Defaults to 0 for unweighted.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        super().add_edge(a, b, weight)
        super().add_edge(b, a, weight)

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        """Remove the bidirectional edge from nodes 'a' to 'b' from the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.

        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        if a != b:
            super().remove_edge(b, a)
        super().remove_edge(a, b)
