import pytest

class SyncedFilePublic:
    def __init__(self, f):
        self.f = f
        self.uploaded = False

    def upload(self):
        if self.uploaded:
            raise RuntimeError("Already uploaded-public")
        self.uploaded = True

def test_syncedfile_public_initial_state():
    sf = SyncedFilePublic("f.txt")
    assert sf.f == "f.txt"
    assert sf.uploaded is False

def test_syncedfile_public_upload_sets_flag():
    sf = SyncedFilePublic("t.txt")
    sf.upload()
    assert sf.uploaded is True

def test_syncedfile_public_upload_twice_errors():
    sf = SyncedFilePublic("dup.txt")
    sf.upload()
    with pytest.raises(RuntimeError) as excinfo:
        sf.upload()
    assert "Already uploaded-public" in str(excinfo.value)