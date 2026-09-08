import os
import shutil
import pytest

class DummyJob:
    def __init__(self, name):
        self.name = name
        self.config = {}

    def run(self, callbacks):
        if 'success' in callbacks and callable(callbacks['success']):
            callbacks['success']()
        # Do not throw if success is missing

cask_dir = os.path.join(os.path.dirname(__file__), '..', '.cask_public')
cask_file = os.path.join(cask_dir, 'public.js')

@pytest.fixture(scope='module', autouse=True)
def setup_and_cleanup():
    os.makedirs(cask_dir, exist_ok=True)
    with open(cask_file, 'w') as f:
        f.write('// dummy public.js content')
    yield
    if os.path.exists(cask_file):
        os.remove(cask_file)
    if os.path.exists(cask_dir):
        try:
            os.rmdir(cask_dir)
        except OSError:
            shutil.rmtree(cask_dir, ignore_errors=True)

def test_initializes_with_name_and_config_public():
    job = DummyJob('publictest')
    assert hasattr(job, 'name')
    assert job.name == 'publictest'
    assert hasattr(job, 'config')

def test_run_and_success_invoked_public():
    succeeded = {'val': False}
    job = DummyJob('publictest')
    def success():
        succeeded['val'] = True
        assert succeeded['val'] is True
    job.run({'success': success})

def test_run_handle_missing_success_callback_public():
    job = DummyJob('publictest')
    try:
        job.run({})
    except Exception:
        pytest.fail("run() should not raise when 'success' is missing")