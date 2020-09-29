import os
import pytest


@pytest.fixture
def script_path():
    def load_script(script_name):
        mod_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(mod_dir, "scripts", script_name)


@pytest.fixture(scope='module')
def max_workers():
    return 4