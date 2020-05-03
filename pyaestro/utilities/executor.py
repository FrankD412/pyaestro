"""Executor utility module for locally scheduled tasks."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
import _io
from subprocess import Popen
from uuid import uuid4

from pyaestro.abstracts.metaclasses import Singleton, SynchronizedClass
from pyaestro.structures import MultiRdrWtrDict


class ExecTaskState(Enum):
    """An enumeration of possible states for Executor tasks."""
    SUCCESS = 0
    INITIALIZED = 1
    PENDING = 2
    RUNNING = 3
    CANCELLED = 4
    FAILED = 5
    UNKNOWN = 6


class ExecCancel(Enum):
    """An enumeration of possible cancellation returns."""
    SUCCESS = 0
    FAILED = 1
    JOBNOTFOUND = 2
    TIMEDOUT = 3


class ExecSubmit(Enum):
    """An enumeration of possible submission returns."""
    SUCCESS = 0
    FAILED = 1


class Executor(metaclass=Singleton):
    """A class that manages local tasks using asynchronous futures."""

    @dataclass
    class _Record(metaclass=SynchronizedClass):
        """Executor Record class for tracking futures and processes."""
        uuid:    uuid4
        process: Popen
        stdout:  _io.TextIOWrapper
        stderr:  _io.TextIOWrapper
        estatus: int
        state:  ExecTaskState

        def __init__(self):
            """Initialize a new record with a uuid and initial state."""
            self.uuid = uuid4()
            self.state = ExecTaskState.INITIALIZED
            self.process = None

        def execute(self, script, cwd, *args, **kwargs):
            """
            Executes the record instance.

            :param script: Path to a script to execute.
            :param cwd: Directory path to execute the script in.
            :param args: Additonal arguments to pass to the script being
             executed.
            :param kwargs: Additional kwargs to configure of execution.
             - shell [bool]: Execute script in a new shell.
             - env [dict]: A dict of environment variables.
             - stdout [str]: Name of the output .out file.
             - stderr [str]: Name of the output .err file.
            """
            try:
                # Pop optional kwargs
                shell = kwargs.pop("shell", True)
                env = kwargs.pop("env", None)
                stdout = kwargs.pop("stdout", f"{self.uuid}.out")
                stderr = kwargs.pop("stderr", f"{self.uuid}.err")

                # Set up core arguments (cmd, stdout, stderr)
                cmd = " ".join([script] + list(*args))
                self.stdout = open(stdout, "wb")
                self.stderr = open(stderr, "wb")

                # Start the new process.
                self.process = \
                    Popen(
                        cmd,
                        shell=shell, env=env, cwd=cwd,
                        stdout=self.stdout, stderr=self.stderr,
                        **kwargs)

                # Initalize the record's state to RUNNING since
                # Popen was called.
                self.state = ExecTaskState.RUNNING
                # Prematurely drop the lock so that other processes
                # can access the class.
                # NOTE: This is a slight nuance of how the metaclass
                # was implemented. Need to figure out if there is a
                # better way to do this.
                self.__lock__.release()
                # Do a non-blocking communicate to wait on the process.
                # DO NOT use a wait -- that blocks and prevents the GIL
                # from moving forward.
                self.process.communicate()

            except Exception:
                raise

        def cancel(self):
            """
            Cancel the task represented by the _Record instance.

            :returns: An ExecCancel enum representing the exit status
             of the cancel command.
            """

            if self.state == ExecTaskState.RUNNING:
                try:
                    self.process.kill()
                    self.process.wait(timeout=20)
                    self.state = ExecTaskState.CANCELLED
                    return ExecCancel.SUCCESS
                except TimeoutError:
                    self.state = ExecTaskState.UNKNOWN
                    return ExecCancel.TIMEDOUT
                except Exception:
                    self.state = ExecTaskState.UNKNOWN
                    return ExecCancel.FAILED

        def cleanup(self):
            """Clean up method to close out a record instance."""
            if self.state == ExecTaskState.CANCELLED:
                return

            self.estatus = self.process.wait()

            if self.estatus != 0:
                self.state = ExecTaskState.FAILED
            else:
                self.state = ExecTaskState.SUCCESS

            # Clean up open log pointers.
            self.stdout.close()
            self.stderr.close()

        @staticmethod
        def cleanup_hook(future):
            """
            Wrap futures with _Record instances for post hooks.

            :param future: Future instance to clean up.
            """
            # Call clean up on the record in the future.
            future.record.cleanup()

    def __init__(self, workers):
        """An Executor that mimics scheduler-like behavior locally."""

        self._statuses = MultiRdrWtrDict()
        self._thread_pool = ThreadPoolExecutor(max_workers=workers)

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
        # Create a new _Record instance to track the submission.
        record = Executor._Record()
        # Setup the stdout and stderr logging.
        stdout = kwargs.get("stdout", f"local-{record.uuid}.out")
        stderr = kwargs.get("stderr", f"local-{record.uuid}.err")

        # Set the record's state to pending.
        record.state = ExecTaskState.PENDING
        # Submit the script to our thread pool.
        future = self._thread_pool.submit(
            record.execute,
            script,
            workspace,
            args,
            stdout=stdout,
            stderr=stderr,
            **kwargs
        )
        # Add the record to the returned future.
        future.record = record
        # Add the callback wrapper to the future for clean up.
        future.add_done_callback(self._Record.cleanup_hook)
        # Add the status to the status dictionary.
        self._statuses[str(record.uuid)] = future
        # Return the job identifier.
        return str(record.uuid)

    def cancel(self, taskid):
        """
        Cancel the specified task in the Executor.

        :param taskid: A uuid of the task to be cancelled.
        :returns: An ExecCancel enum representing the exit status
         of the cancel command.
        """
        # If the job identifier isn't status, return JOBNOTFOUND
        if taskid not in self._statuses:
            return ExecCancel.JOBNOTFOUND
        else:
            # We need to check the future to see if it's executing.
            future = self._statuses[taskid]
            # If we find that the future is done, just return success.
            if future.done():
                print("FOUND DONE: SUCCESS")
                return ExecCancel.SUCCESS
            # If we haven't started running yet, cancel from the future.
            elif not future.running():
                print("NOT RUNNING << PENDING")
                future.record.state = ExecTaskState.CANCELLED
                future.cancel()
                return ExecCancel.SUCCESS
            else:
                print("RUNNING")
                # Otherwise, return the status of the cancel call.
                return self._statuses[taskid].record.cancel()

    def cancel_all(self):
        for task in self._statuses.keys():
            self.cancel(task)

    def get_status(self, taskid):
        """
        Get the status of a specific task.

        :param taskid: A string containing the task identifier.
        :returns: A ExecTaskState set the current state of the task.
        """
        return self._statuses[taskid].record.state

    def get_all_status(self):
        """
        Get the status of a all tasks.

        :returns: Generator of tuples as (taskid, ExecTaskState).
        """
        for uuid, future in self._statuses.items():
            yield uuid, future.record.state
