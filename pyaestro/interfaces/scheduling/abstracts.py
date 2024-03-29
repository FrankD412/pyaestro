"""A module that defines interfaces for interacting with schedulers."""
from abc import ABC, abstractmethod


class SchedulerAdapter(ABC):
    """An interface for interacting with system schedulers."""

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Create an instance to interface with a scheduler.

        :params kwargs: Settings for this instance of adapter.
        """
        raise NotImplementedError

    @abstractmethod
    def get_header(self, shell, resources):
        """
        Generate the header for a scheduler script of this type.
        """
        raise NotImplementedError

    @abstractmethod
    def submit(self, script, workspace, **kwargs):
        """
        Submit a script to the system scheduler for execution.

        :params script: Path to the script to submit.
        :params workspace: Working directory for execution.
        :returns: A SubmissionRecord instance.
        """
        raise NotImplementedError

    @abstractmethod
    def job_status(self, jobid):
        """
        Check the status of a single job.

        :params jobid: String containing a job identifier.
        :returns: An enumerated job status.
        """
        raise NotImplementedError

    @abstractmethod
    def joblist_status(self, joblist):
        """
        Check the status of a list of jobs.

        :params joblist: A list containing strings of job identifiers.
        :returns: A dictionary mapping jobid to job status.
        """
        raise NotImplementedError
