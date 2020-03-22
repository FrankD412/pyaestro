from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class StepRecord:
    """A class to track a tasks state and record timing information"""
    name: str
    base_name: str
    combination: str

    time_ledger: dict
    cur_state: StateEnum
