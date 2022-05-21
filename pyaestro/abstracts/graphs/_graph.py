"""A module of different graph types and other properties."""
from __future__ import annotations

import functools
import json
from abc import ABC, abstractmethod
from os.path import abspath, dirname, join
from types import TracebackType
from typing import Callable, Dict, Hashable, Iterable, Type

import jsonschema

from pyaestro.bases import Specifiable
from pyaestro.dataclasses import GraphEdge
from pyaestro.typing import Comparable

SCHEMA_DIR = join(dirname(dirname(abspath(__file__))), "_schemas")


class Graph(Specifiable, ABC):

    _write_only_methods = (
        "__setitem__",
        "add_edge",
        "delete_edges",
        "remove_edge",
        "__delitem__",
    )
    with open(join(SCHEMA_DIR, "graph.json")) as schema:
        _dict_schema = json.load(schema)

    @classmethod
    def _read_only(cls, method: Callable):
        @functools.wraps(method)
        def locked_function(*args, **kwargs):
            self = args[0]
            if self._locked:
                raise RuntimeError(
                    f"Unable to call method '{method.__name__}' while in "
                    "read-only context."
                )
            return method(*args, **kwargs)

        return locked_function

    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        print(cls.__setitem__)
        cls.__setitem__ = cls._read_only(cls.__setitem__)
        print(cls.__delitem__)
        cls.__delitem__ = cls._read_only(cls.__setitem__)
        print(cls.remove_edge)
        cls.remove_edge = cls._read_only(cls.remove_edge)
        cls.add_edge = cls._read_only(cls.add_edge)

    def __init__(self):
        self._vertices = {}
        self._locked = False

    def __contains__(self, key: Hashable) -> bool:
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

    def __enter__(self) -> Graph:
        self._locked = True
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._locked = False
        if exc_val:
            raise exc_val

    @classmethod
    def from_specification(
        cls, specification: Dict[Hashable, Dict[Hashable, object]]
    ) -> Type[Graph]:
        """Construct a Graph based on a specification of edges and vertices.

        Args:
            specification (Dict[Hashable, Dictionary[Hashable, object]]):
            A dictionary containing two keys:
                edges: A dictionary of neighbors for each vertex containing
                    a list of (neighbor, weight) tuples.
                vertices: A dictionary mapping keys to their values.

        Returns:
            Type[Graph]: An instance of the type Graph.

        Raises:
            ValidationError: Raised when specification does not match the fixed
            schema for a Graph.
        """
        graph = cls()
        jsonschema.validate(specification, schema=cls._dict_schema)

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
    def edges(self) -> Iterable[GraphEdge]:
        """Iterate the edges of a graph.

        Returns:
            Iterable[GraphEdge]: An iterable of tuples containing edges.
        """
        raise NotImplementedError

    @abstractmethod
    def add_edge(
        self, a: Hashable, b: Hashable, weight: Comparable = 0
    ) -> None:
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
    def get_neighbors(self, key: Hashable) -> Iterable[GraphEdge]:
        """Get the connected neighbors of the specified node.

        Args:
            a (Hashable): Key whose neighbor's should be returned.

        Raises:
            KeyError: Raised when 'key' does not exist in the graph.

        Returns:
            Iterable[GraphEdge]: An iterable of GraphEdge records that
            represent the neighbors of the vertex named 'key'.
        """
        raise NotImplementedError
