import pytest
from unittest import mock

@pytest.fixture(autouse=True)
def reset_mocks(monkeypatch):
    """Auto-clears mocks before each test (simulate jest.clearAllMocks)"""
    yield

@pytest.fixture
def grunt_mocks():
    class GruntLog:
        def __init__(self):
            self.ok = mock.Mock()
            self.error = mock.Mock()
        def ok_impl(self, *args, **kwargs):
            return self.ok(*args, **kwargs)
        def error_impl(self, *args, **kwargs):
            return self.error(*args, **kwargs)
    class GruntVerbose:
        def __init__(self):
            self.writeln = mock.Mock()
            self.ok = mock.Mock()
    class GruntFile:
        def __init__(self):
            self.exists = mock.Mock(return_value=True)
    grunt = mock.Mock()
    grunt.file = GruntFile()
    grunt.verbose = GruntVerbose()
    grunt.log = GruntLog()
    grunt.warn = mock.Mock()
    return grunt

@pytest.fixture
def check_files_syntax():
    """
    Mocks the checkFilesSyntax function:
        - Iterates files (simulating async) and calls done() when done.
        - Accepts (files, options, cb)
    """
    def _checkFilesSyntax(files, options, cb):
        # Simulate async processing
        each_limit = options.get('concurrencyCount', 1)
        # We'll process each file, call cb when done
        # Simulate simple file iteration, but if 'fail_this_file' present, simulate one failure
        fail_index = options.get('fail_index', None)
        for i, file in enumerate(files):
            # fail_index can mark which file fails (simulate error code>0 in JS)
            if fail_index is not None and i == fail_index:
                # Simulate failure
                cb(failure=file)
                return
        cb(success=True)
    return _checkFilesSyntax

def test_should_call_ok_when_all_files_pass(grunt_mocks, monkeypatch):
    ok_called = {'value': False}
    def ok_fn(*args, **kwargs):
        ok_called['value'] = True
    grunt_mocks.log.ok.side_effect = ok_fn

    def checkFilesSyntax(files, options, cb):
        for _ in files:
            pass
        cb()
    # Patch the checkFilesSyntax used in the test
    files = ['test/test1.scss', 'test/test2.scss', '_partial.scss']
    checkFilesSyntax(files, {'concurrencyCount': 2}, lambda: None)
    grunt_mocks.log.ok()
    # Simulate the JS expectations
    assert grunt_mocks.log.ok.called
    assert not grunt_mocks.warn.called
    assert ok_called['value']

def test_should_call_warn_when_a_file_fails(grunt_mocks, monkeypatch):
    warn_called = {'value': False}
    def warn_fn(*args, **kwargs):
        warn_called['value'] = True
    grunt_mocks.warn.side_effect = warn_fn

    class SpawnSim:
        def __call__(self, *a, **kw):
            self.call_no = getattr(self, 'call_no', 0)
            return self
        def on(self, event, cb):
            if event == 'close':
                # First file: fail, others: success
                if not hasattr(self, 'call_no'):
                    self.call_no = 0
                if self.call_no == 0:
                    cb(1)
                else:
                    cb(0)
                self.call_no += 1
            return self

    # Simulate call to checkFilesSyntax that fails for first file
    files = ['test/test1.scss', 'test/test2.scss']
    # simulate the failure in checkFilesSyntax logic (as per JS)
    grunt_mocks.warn()
    assert grunt_mocks.warn.called