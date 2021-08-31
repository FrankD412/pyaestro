import pytest

import pyaestro.utilities.executor as executor


@pytest.fixture(scope='function')
def configure_executor(max_workers, num_ok, num_run, num_fail, num_total):
    executor.Executor(max_workers)


class TestExecutor:
    pass
