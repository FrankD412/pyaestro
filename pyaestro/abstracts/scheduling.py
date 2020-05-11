"""A module that defines interfaces for interacting with schedulers."""
from abc import ABC, ABCMeta, abstractmethod
from enum import Enum

from pyaestro.abstracts.metaclasses import Singleton


class SubmissionCode(Enum):
    SUCCESS = 0
    FAILURE = 1


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

class _SingletonABC(ABCMeta, Singleton):
    pass


class Executor(ABC):
    """An interface for classes that manages local tasks."""

    @abstractmethod
    def __init__(self, workers):
        """An Executor that mimics scheduler-like behavior locally."""

    @abstractmethod
    def submit(self, script, workspace, *args, **kwargs):
        """
        Executes a script within an Executor instance.

        :param script: Path to a script to execute.
        :param cwd: Directory path to execute the script in.
        :param args: Additonal arguments to pass to the script being
            executed.
        :param kwargs: Additional kwargs to configure of execution.
            - shell [bool]: Execute script in a new shell.
            - env [dict]: A dict of environment variables.
            - stdout [str]: Name of the output .out file.
            - stderr [str]: Name of the output .err file.
        :returns: A string containing the unique job identifier.
        """

    @abstractmethod
    def cancel(self, taskid):
        """
        Cancel the specified task in the Executor.

        :param taskid: A uuid of the task to be cancelled.
        :returns: An ExecCancel enum representing the exit status
         of the cancel command.
        """

    @abstractmethod
    def cancel_all(self):
        """
        Cancel all tasks an Executor is managing.

        :returns: An ExecCancel enum representing the exit status
         of the cancel command.
        """

    @abstractmethod
    def get_status(self, taskid):
        """
        Get the status of a specific task.

        :param taskid: A string containing the task identifier.
        :returns: A ExecTaskState set the current state of the task.
        """

    @abstractmethod
    def get_all_status(self):
        """
        Get the status of a all tasks.

        :returns: Generator of tuples as (taskid, ExecTaskState).
        """


class SingletonExecutor(Executor, metaclass=_SingletonABC):
    pass

class SchedulerAdapter(ABC):
    """An interface for interacting with system schedulers."""

    @abstractmethod
    def __init__(self, **kwargs):
        """
        Create an instance to interface with a scheduler.

        :params kwargs: Settings for this instance of adapter.
        """

    @abstractmethod
    def get_header(self, shell, resources):
        """
        Generate the header for a scheduler script of this type.
        """

    @abstractmethod
    def submit(self, script, workspace, **kwargs):
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
