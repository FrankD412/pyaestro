"""A module that defines interfaces for interacting with schedulers."""
from abc import ABC, abstractclassmethod
from enum import Enum
from pathlib import Path
from typing import Dict, List, Union


class TaskState(Enum):
    """An enumeration for task state."""
    BLOCKED = 0
    PENDING = 1
    WAITING = 2
    RUNNING = 3
    FINISHED = 4
    FAILED = 5
    INCOMPLETE = 6
    HWFAILURE = 7
    TIMEDOUT = 8
    UNKNOWN = 9
    CANCELLED = 10


IDENTIFIER_HINT = Union[str, int]
JOBLIST_HINT = Union[List[int], List[str]]
STATUS_HINT = Union[Dict[int, TaskState], Dict[str, TaskState]]


class SchedulerMixIn(ABC):
    """An interface for interacting with system schedulers."""

    @abstractclassmethod
    def submit(cls, command: str, workspace: Path, **kwargs):
        """
        Submit a script to the system scheduler for execution.

        :params script: Path to the script to submit.
        :params workspace: Working directory for execution.
        :returns: A SubmissionRecord instance.
        """

    @abstractclassmethod
    def job_status(cls, identifier: IDENTIFIER_HINT) -> TaskState:
        """
        Check the status of a single job.

        :params jobid: String containing a job identifier.
        :returns: An enumerated job status.
        """

    @abstractclassmethod
    def joblist_status(cls, joblist: JOBLIST_HINT) -> STATUS_HINT:
        """
        Check the status of a list of jobs.

        :params joblist: A list containing strings of job identifiers.
        :returns: A dictionary mapping jobid to job status.
        """


class SchedulerHeaderMixIn(ABC):
    """PASS"""

    @abstractclassmethod
    def get_header(self, shell: Path, resources):
        """
        Generate the header for a scheduler script of this type.
        """