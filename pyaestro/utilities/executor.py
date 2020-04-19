from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
import _io
from os.path import basename, join, splitext
from subprocess import Popen
from uuid import uuid4

from pyaestro.abstracts import Singleton
from pyaestro.structures import MultiRdrWtrDict
from . import synchronizedclass


class ExecTaskState(Enum):
    PENDING = 0
    RUNNING = 1
    CANCELLED = 2
    SUCCESS = 3
    FAILED = 4


class ExecCancel(Enum):
    SUCCESS = 0
    FAILED = 1
    JOBNOTFOUND = 2


class Executor(metaclass=Singleton):

    @dataclass(init=False)
    @synchronizedclass
    class _Record:
        uuid:    uuid4
        process: Popen
        future:  Future
        stdout:  _io.TextIOWrapper
        stderr:  _io.TextIOWrapper
        estatus: int
        state:  ExecTaskState

        def __init__(self, uuid):
            self.uuid = uuid
            self.state = ExecTaskState.PENDING

        def cancel(self):
            pass

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

    def _execute(self, script, cwd, record, **kwargs):
        shell = kwargs.pop("shell", True)
        env = kwargs.pop("env", None)

        script_name = join(cwd, splitext(basename(script)))
        stdout = kwargs.get("stdout", f"{script_name}.out")
        stderr = kwargs.get("stderr", f"{script_name}.err")
        record.stdout = open(stdout, "wb")
        record.stderr = open(stderr, "wb")

        record.process = \
            Popen(
                script,
                shell=shell, env=env, cwd=cwd,
                stdout=record.stdout, stderr=record.stderr,
                **kwargs)

        record.state = ExecTaskState.RUNNING
        self._statuses[str(record.uuid)] = record
        record.process.wait()

    def submit(self, script, workspace, **kwargs):
        record = Executor._Record(uuid4())
        stdout = kwargs.pop("stdout", None)
        stderr = kwargs.pop("stderr", None)

        record.future = \
            self._thread_pool.submit(
                self._execute,
                script,
                workspace,
                record,
                stdout,
                stderr,
                **kwargs
            )
        record.future.add_done_callback(record.cleanup_hook)
        return str(record.uuid)

    def cancel(self, taskid):
        if taskid not in self._statuses:
            return ExecCancel.JOBNOTFOUND
        
        try:
            self._statuses[taskid].cancel()
            return ExecCancel.SUCCESS
        except:
            return ExecCancel.FAILED

    def cancel_all(self):
        pass

    def get_status(self, taskid):
        return self._statuses[taskid].state
