"""A module dedicated to data records."""
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

from pyaestro.abstracts.scheduling import TaskState


@dataclass
class TaskRecord:
    """A class to track a tasks state and record timing information"""
    name: str
    base_name: str
    combination: str

    time_ledger: defaultdict(datetime.now)
    cur_state: TaskState

    def mark_state(self, state):
        """Mark the state of the step and the time it was marked."""
        if not isinstance(state, TaskState):
            raise TypeError("Expected a state of type StepState.")

        self.time_ledger[state]
        self.cur_state = state

    def time_diff(self, state_a, state_b):
        pass

    def write_script(self, path, adapter):
        pass

    def execute(self, cmd, adapter):
        pass