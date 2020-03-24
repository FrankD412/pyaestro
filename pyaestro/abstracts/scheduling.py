"""A module that defines interfaces for interacting with schedulers."""
from abc import ABC, abstractmethod
from enum import Enum


class SubmissionCode(Enum):
    SUCCESS = 0
    FAILURE = 1


class SchedulerAdapter(ABC):
    """An interface for interacting with system schedulers."""

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Create an instance to interface with a scheduler.

        :params kwargs: Settings for this instance of adapter.
        """

    @abstractmethod
    def get_header(self, resources):
        """
        Generate the header for a scheduler script of this type.
        """

    @abstractmethod
    def submit(self, script, workspace):
        """
        Submit a script to the system scheduler for execution.

        :params script: Path to the script to submit.
        :params workspace: Working directory for execution.
        :returns: A SubmissionRecord instance.
        """

    @abstractmethod
    def job_status(self, jobid):
        """
        Check the status of a single job.

        :params jobid: String containing a job identifier.
        :returns: An enumerated job status.
        """

    @abstractmethod
    def joblist_status(self, joblist):
        """
        Check the status of a list of jobs.

        :params joblist: A list containing strings of job identifiers.
        :returns: A dictionary mapping jobid to job status.
        """
