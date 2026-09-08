import pytest

class SyncedFileMock:
    def __init__(self, path):
        self.path = path
        self.globbed = False
        self.remoted = False
        self.ff = False
        self.fr = False
        self.fake_action = {'action': 'ok', 'path': path}
    def globDone(self):
        self.globbed = True
    def remoteDone(self):
        self.remoted = True
    def foundFile(self, *a, **k):
        self.ff = True
    def foundRemote(self, *a, **k):
        self.fr = True

class SyncedFileCollection:
    def __init__(self):
        self.files = {}
        self.glob_done = False
        self.remote_done = False
    def foundFile(self, path):
        if self.glob_done:
            raise RuntimeError("Glob is supposed to be done")
        if path not in self.files:
            self.files[path] = SyncedFileMock(path)
        self.files[path].foundFile()
    def foundRemote(self, path, h=None):
        if self.remote_done:
            raise RuntimeError("Remote listing is supposed to be done")
        if path not in self.files:
            self.files[path] = SyncedFileMock(path)
        self.files[path].foundRemote()
    def globDone(self):
        if self.glob_done:
            raise RuntimeError("Glob is supposed to be done")
        self.glob_done = True
        for f in self.files.values():
            f.globDone()
    def remoteDone(self):
        if self.remote_done:
            raise RuntimeError("Remote listing is supposed to be done")
        self.remote_done = True
        for f in self.files.values():
            f.remoteDone()
    @property
    def allDone(self):
        return [self.files[path].fake_action for path in self.files]

def test_foundfile_foundremote_actions():
    coll = SyncedFileCollection()
    coll.foundFile('foo.txt')
    coll.foundRemote('bar.txt', 'h123')
    # The attributes will be set on the respective SyncedFileMock
    assert coll.files['foo.txt'].ff is True
    assert coll.files['bar.txt'].fr is True
    coll.globDone()
    coll.remoteDone()
    actions = coll.allDone
    assert isinstance(actions, list)
    assert coll.files['foo.txt'].globbed is True
    assert coll.files['bar.txt'].globbed is True
    assert coll.files['foo.txt'].remoted is True
    assert coll.files['bar.txt'].remoted is True

def test_throw_if_globdone_or_remotedone_twice():
    coll = SyncedFileCollection()
    coll.globDone()
    with pytest.raises(RuntimeError):
        coll.globDone()
    c2 = SyncedFileCollection()
    c2.remoteDone()
    with pytest.raises(RuntimeError):
        c2.remoteDone()

def test_throw_if_foundfile_after_globdone():
    coll = SyncedFileCollection()
    coll.globDone()
    with pytest.raises(RuntimeError):
        coll.foundFile('foo.txt')

def test_throw_if_foundremote_after_remotedone():
    coll = SyncedFileCollection()
    coll.remoteDone()
    with pytest.raises(RuntimeError):
        coll.foundRemote('foo.txt', 'h')

def test_foundfile_after_both_dones_calls_both():
    coll = SyncedFileCollection()
    coll.globDone()
    coll.remoteDone()
    # Should not throw and should call both .globDone and .remoteDone on new SyncedFileMock
    coll.foundFile('later.txt')
    assert coll.files['later.txt'].globbed is True
    assert coll.files['later.txt'].remoted is True