import pytest

class SyncedFile:
    def __init__(self, file_path, uploaded=False):
        self.file_path = file_path
        self.uploaded = uploaded
        self.size = len(file_path)  # fake size

    def mark_uploaded(self):
        if self.uploaded:
            raise Exception("Already uploaded")
        self.uploaded = True

def test_syncedfile_constructor_sets_initial_state():
    sf = SyncedFile("some/file/path.txt")
    assert sf.file_path == "some/file/path.txt"
    assert sf.uploaded is False
    assert sf.size == len("some/file/path.txt")

def test_syncedfile_mark_uploaded_sets_flag():
    sf = SyncedFile("zzz")
    sf.mark_uploaded()
    assert sf.uploaded is True

def test_syncedfile_mark_uploaded_twice_raises():
    sf = SyncedFile("xxx")
    sf.mark_uploaded()
    with pytest.raises(Exception) as excinfo:
        sf.mark_uploaded()
    assert "Already uploaded" in str(excinfo.value)