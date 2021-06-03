"""A module of different graph types and other properties."""
from __future__ import annotations
from abc import ABC, abstractmethod
import json
import jsonschema
from os.path import abspath, dirname, join
from typing import Dict, Hashable, Iterable, Tuple, Type

from pyaestro.bases import Specifiable

SCHEMA_DIR = join(dirname(abspath(__file__)), "_schemas")

class Graph(Specifiable, ABC):

    with open(join(SCHEMA_DIR, "graph.json")) as schema:
        _dict_schema = json.load(schema)

    def __init__(self):
        self._vertices = {}

    def __contains__(self, key) -> bool:
        return self._vertices.__contains__(key)

    def __getitem__(self, key):
        if key not in self._vertices:
            raise KeyError(f"Key '{key}' is not in graph.")

        return self._vertices.get(key)

    def __setitem__(self, key: Hashable, value: object) -> None:
        self._vertices[key] = value

    def __delitem__(self, key: Hashable) -> None:
        if key not in self._vertices:
            raise KeyError(f"Key '{key}' is not in graph.")

        del self._vertices[key]
        self.delete_edges(key)

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
                - edges: A dictionary of lists mapping nodes to their neighbors.
                - vertices: A dictionary mapping keys to their values (objects).

        Returns:
            Type[Graph]: An instance of the type Graph.
            
        Raises:
            ValidationError: Raised when specification does not match the fixed
            schema for a Graph.
        """

        graph = cls()
        jsonschema.validate(specification, schema=cls._dict_schema)

        graph._vertices = specification["vertices"]

        for node, neighbors in specification["edges"].items():
            for neighbor in neighbors:
                graph.add_edge(node, neighbor)
                
        return graph

    @abstractmethod
    def delete_edges(self, key: Hashable) -> None:
        """Delete all edges associated to a key from the Graph.

        Args:
            key (Hashable): Key to a node whose edges are to be removed. 
        """
        ...

    @abstractmethod
    def edges(self) -> Iterable[Tuple[Hashable]]:
        """Iterate the edges of a graph.

        Returns:
            Iterable[Tuple[Hashable]]: An iterable of tuples containing edges.
        """
        ...

    @abstractmethod
    def add_edge(self, a: Hashable, b: Hashable) -> None:
        """Add an edge to the graph.

        Args:
            a (Hashable): Key identifying side 'a' of an edge.
            b (Hashable): Key identifying side 'b' of an edge.
        
        Raises:
            KeyError: Raised when either node 'a' or node 'b'
            do not exist in the graph.
        """
        ...

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
        ...

    @abstractmethod
    def get_neighbors(self, key: Hashable) -> Iterable[Hashable]:
        """Get the connected neighbors of the specified node.

        Args:
            a (Hashable): Key whose neighbor's should be returned.
        
        Raises:
            KeyError: Raised when 'key' does not exist in the graph.
        """
        ...

