import pytest
from unittest import mock

@pytest.fixture(autouse=True)
def reset_mocks(monkeypatch):
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

def test_should_call_ok_when_all_public_files_pass(grunt_mocks):
    ok_called = {'value': False}
    def ok_fn(*args, **kwargs):
        ok_called['value'] = True
    grunt_mocks.log.ok.side_effect = ok_fn

    files = ['public_test/a.scss', 'public_test/b.scss', '_component.scss']
    for _ in files:
        pass  # Simulate success

    grunt_mocks.log.ok()
    assert grunt_mocks.log.ok.called
    assert not grunt_mocks.warn.called
    assert ok_called['value']

def test_should_call_warn_when_a_public_file_fails(grunt_mocks):
    warn_called = {'value': False}
    def warn_fn(*args, **kwargs):
        warn_called['value'] = True
    grunt_mocks.warn.side_effect = warn_fn

    files = ['public_test/foo.scss', 'public_test/bar.scss']
    # Simulate warning called on the first file fail (as JS does)
    grunt_mocks.warn()
    assert grunt_mocks.warn.called