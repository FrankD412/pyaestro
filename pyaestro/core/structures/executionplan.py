from pathlib import Path

from ..graphs import MultiGraph, EdgeType


class ExecutionPlan:
    def __init__(self, name: str, root_workspace: Path):
        self._name = name
        self._workspace = root_workspace

        # Initialize the task graph
        self._task_graph = MultiGraph()
        self._task_graph.add_layer("data", EdgeType.FORWARD_DIRECTIONAL)

    def add_task(self, task):
        ...
