import pytest
from unittest import mock
from unittest.mock import MagicMock, patch
import os
import tempfile
import io

class Worker:
    def __init__(self, activity):
        self.activity = activity
        self.uri = None
        self.file_path = None
        self.binary_path = None

    def runWithNewProcessReturn(self, arg1, command):
        return "root xzr"

    def runWithNewProcessNoReturn(self, arg1, command):
        pass

    def rootAvailable(self):
        try:
            out = self.runWithNewProcessReturn(True, "id")
            if out is not None and "root" in out:
                return True
            else:
                return False
        except Exception:
            return False

    def copy(self):
        # would access activity.getContentResolver
        resolver = self.activity.getContentResolver()
        return resolver

    def getBinary(self):
        # file_path and binary_path must be set
        if not (self.file_path and self.binary_path and os.path.exists(self.file_path)):
            raise IOError("File not found")
        self.runWithNewProcessNoReturn(True, "some_command")

    def patch(self):
        self.runWithNewProcessNoReturn(True, "some_command")

    def flash(self, activity):
        self.runWithNewProcessReturn(True, "some_command")

@pytest.fixture(autouse=True)
def reset_status():
    pass

def test_root_available_true():
    mock_activity = MagicMock()
    worker = Worker(mock_activity)
    with patch.object(worker, 'runWithNewProcessReturn', return_value="root xzr"):
        assert worker.rootAvailable()

def test_root_available_false():
    mock_activity = MagicMock()
    worker = Worker(mock_activity)
    with patch.object(worker, 'runWithNewProcessReturn', side_effect=IOError()):
        assert not worker.rootAvailable()

def test_copy_throws():
    mock_activity = MagicMock()
    worker = Worker(mock_activity)
    with patch.object(mock_activity, 'getContentResolver', side_effect=IOError("fail")):
        with pytest.raises(Exception):
            worker.copy()

def test_get_binary_not_exist():
    mock_activity = MagicMock()
    worker = Worker(mock_activity)
    with patch.object(worker, 'runWithNewProcessNoReturn'):
        worker.file_path = os.path.join(tempfile.gettempdir(), "notfound.zip")
        worker.binary_path = os.path.join(tempfile.gettempdir(), "notfound.update-binary")
        with pytest.raises(IOError):
            worker.getBinary()

def test_patch_assetsutil_throws():
    mock_activity = MagicMock()
    worker = Worker(mock_activity)
    with patch.object(worker, 'runWithNewProcessNoReturn', side_effect=IOError("fail")):
        with pytest.raises(IOError):
            worker.patch()

def test_flash_throws():
    mock_activity = MagicMock()
    worker = Worker(mock_activity)
    with patch.object(worker, 'runWithNewProcessReturn', side_effect=IOError("fail")):
        with pytest.raises(IOError):
            worker.flash(mock_activity)