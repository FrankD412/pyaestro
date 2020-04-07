"""A module dedicated to data records."""
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
from enum import Enum


class StepState(Enum):
    """States that a workflow step can reside in."""
    INITIALIZED = 0
    QUEUED = 1
    WAITING = 2
    RUNNING = 3
    FINISHING = 4
    FINISHED = 5
    FAILED = 6
    INCOMPLETE = 7
    HWFAILURE = 8
    TIMEDOUT = 9
    UNKNOWN = 10
    CANCELLED = 11


@dataclass
class StepRecord:
    """A class to track a tasks state and record timing information"""
    name: str
    base_name: str
    combination: str

    time_ledger: defaultdict(datetime.now)
    cur_state: StepState

    def mark_state(self, state):
        """Mark the state of the step and the time it was marked."""
        if not isinstance(state, StepState):
            raise TypeError("Expected a state of type StepState.")

        self.time_ledger[state]
        self.cur_state = state

    def time_diff(self, state_a, state_b):
        pass

    def write_script(self, path, adapter):
        pass

    def execute(self, cmd, adapter):
        pass