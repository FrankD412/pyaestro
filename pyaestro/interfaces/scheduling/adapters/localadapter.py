"""A module for local execution."""
from pyaestro.abstracts.scheduling import SchedulerAdapter


class LocalAdapter(SchedulerAdapter):
    """An interface for executing local processes."""

    def __init__(self, settings):
        """
        Create an instance to interface with a scheduler.

        :params kwargs: Settings for this instance of adapter.
        """
        ...

    def get_header(self, resources):
        """
        Generate the header for a scheduler script of this type.
        """
        ...

    def submit(self, script, workspace):
        """
        Submit a script to the system scheduler for execution.

        :params script: Path to the script to submit.
        :params workspace: Working directory for execution.
        :returns: A SubmissionRecord instance.
        """
        ...

    def job_status(self, jobid):
        """
        Check the status of a single job.

        :params jobid: String containing a job identifier.
        :returns: An enumerated job status.
        """
        ...

    def joblist_status(self, joblist):
        """
        Check the status of a list of jobs.

        :params joblist: A list containing strings of job identifiers.
        :returns: A dictionary mapping jobid to job status.
        """
        ...
