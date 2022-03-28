from typing import Hashable, Iterable, Tuple

from pyaestro.abstracts.graphs import Graph
from pyaestro.typing import Comparable


class ConcreteAbstractGraph(Graph):
    def _delete_edges(self, key: Hashable) -> None:
        pass

    def edges(self) -> Iterable[Tuple[Hashable]]:
        pass

    def add_edge(
        self, a: Hashable, b: Hashable, weight: Comparable = 0
    ) -> None:
        pass

    def remove_edge(self, a: Hashable, b: Hashable) -> None:
        pass

    def delete_edges(self, key: Hashable) -> None:
        pass

    def get_neighbors(self, node: Hashable) -> Iterable[Hashable]:
        raise StopIteration
