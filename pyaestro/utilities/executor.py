from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
import _io
from os.path import basename, join, splitext
from subprocess import Popen
from uuid import uuid4

from pyaestro.abstracts.metaclasses import Singleton, SynchronizedClass
from pyaestro.structures import MultiRdrWtrDict
# from . import synchronized_class


class ExecTaskState(Enum):
    """An enumeration of possible states for Executor tasks."""
    SUCCESS = 0
    INITIALIZED = 1
    PENDING = 2
    RUNNING = 3
    CANCELLED = 4
    FAILED = 5


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
        future:  Future
        stdout:  _io.TextIOWrapper
        stderr:  _io.TextIOWrapper
        estatus: int
        state:  ExecTaskState

        def __init__(self):
            self.uuid = uuid4()
            self.state = ExecTaskState.INITIALIZED

        def execute(self, script, cwd, record, args, **kwargs):

            try:
                shell = kwargs.pop("shell", True)
                env = kwargs.pop("env", None)
                cmd = [script] + args

                script_name = join(cwd, splitext(basename(script)))
                stdout = kwargs.get("stdout", f"{script_name}.out")
                stderr = kwargs.get("stderr", f"{script_name}.err")
                self.stdout = open(stdout, "wb")
                self.stderr = open(stderr, "wb")

                self.process = \
                    Popen(
                        cmd,
                        shell=shell, env=env, cwd=cwd,
                        stdout=self.stdout, stderr=self.stderr,
                        **kwargs)

                self.state = ExecTaskState.RUNNING
                return ExecSubmit.SUCCESS
            except Exception:
                return ExecSubmit.FAILED

        def cancel(self):
            if self.state == ExecTaskState.PENDING:
                self.future.cancel()
                return ExecCancel.SUCCESS
            elif self.state == ExecTaskState.RUNNING:
                try:
                    self.process.kill()
                    self.process.wait(timeout=20)
                    return ExecCancel.SUCCESS
                except TimeoutError:
                    return ExecCancel.TIMEDOUT
                except:
                    return ExecCancel.FAILED

        def cleanup_hook(self):
            self.estatus = self.process.returncode

            if self.estart != 0:
                self.state = ExecTaskState.FAILED
            else:
                self.state = ExecTaskState.SUCCESS

            # Clean up open log pointers.
            self.stdout.close()
            self.stderr.close()

    def __init__(self, workers):
        self._statuses = MultiRdrWtrDict()
        self._thread_pool = ThreadPoolExecutor(max_workers=workers)


    def submit(self, script, workspace, *args, **kwargs):
        record = Executor._Record()
        stdout = kwargs.pop("stdout", None)
        stderr = kwargs.pop("stderr", None)

        self._statuses[str(record.uuid)] = record
        self._thread_pool.submit(
            record.execute,
            script,
            workspace,
            record,
            args,
            stdout,
            stderr,
            **kwargs
        )

        record.future.add_done_callback(record.cleanup_hook)
        return str(record.uuid)

    def cancel(self, taskid):
        if taskid not in self._statuses:
            return ExecCancel.JOBNOTFOUND
        else:
            return self._statuses[taskid].cancel()

    def cancel_all(self):
        for task in self._statuses.values():
            task.cancel()

    def get_status(self, taskid):
        return self._statuses[taskid].state

    def get_all_status(self):
        return {
            uuid: record.state
            for (uuid, record) in self._statuses.items()
        }