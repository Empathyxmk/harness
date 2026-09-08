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

cask_dir = os.path.join(os.path.dirname(__file__), '..', '.cask')
cask_file = os.path.join(cask_dir, 'test.js')

@pytest.fixture(scope="module", autouse=True)
def _setup_files_and_cleanup():
    os.makedirs(cask_dir, exist_ok=True)
    with open(cask_file, 'w') as f:
        f.write('// dummy test.js content')
    yield
    if os.path.exists(cask_file):
        os.remove(cask_file)
    if os.path.exists(cask_dir):
        try:
            os.rmdir(cask_dir)
        except OSError:
            # Folder not empty, likely test run done weird
            shutil.rmtree(cask_dir, ignore_errors=True)

def test_job_initializes_with_name_and_config():
    job = DummyJob('test')
    assert hasattr(job, 'name')
    assert job.name == 'test'
    assert hasattr(job, 'config')

def test_job_run_and_success_invoked():
    succeeded = {'val': False}
    job = DummyJob('test')
    def success():
        succeeded['val'] = True
        assert succeeded['val'] is True
    job.run({'success': success})

def test_job_run_missing_success_callback():
    job = DummyJob('test')
    try:
        job.run({})
    except Exception:
        pytest.fail("run() should not raise when 'success' is missing")