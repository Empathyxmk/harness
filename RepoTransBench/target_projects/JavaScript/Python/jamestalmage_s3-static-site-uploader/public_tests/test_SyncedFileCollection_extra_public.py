import pytest

class SyncedFileMock:
    def __init__(self, path):
        self.path = path
        self.globbed = False
        self.remoted = False
        self.ff = False
        self.fr = False
        self.action_result = {'action': 'ok', 'path': path}
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
        return [self.files[path].action_result for path in self.files]

def test_foundFile_foundRemote_and_resolve_allDone():
    coll = SyncedFileCollection()
    coll.foundFile('baz.pdf')
    coll.foundRemote('quux.doc', 'h456')
    assert coll.files['baz.pdf'].ff
    assert coll.files['quux.doc'].fr
    coll.globDone()
    coll.remoteDone()
    actions = coll.allDone
    assert isinstance(actions, list)
    assert coll.files['baz.pdf'].globbed
    assert coll.files['quux.doc'].globbed
    assert coll.files['baz.pdf'].remoted
    assert coll.files['quux.doc'].remoted

def test_throw_if_globDone_or_remoteDone_twice():
    coll = SyncedFileCollection()
    coll.globDone()
    with pytest.raises(RuntimeError):
        coll.globDone()
    c2 = SyncedFileCollection()
    c2.remoteDone()
    with pytest.raises(RuntimeError):
        c2.remoteDone()

def test_throw_if_foundFile_after_globDone():
    coll = SyncedFileCollection()
    coll.globDone()
    with pytest.raises(RuntimeError):
        coll.foundFile('qux.png')

def test_throw_if_foundRemote_after_remoteDone():
    coll = SyncedFileCollection()
    coll.remoteDone()
    with pytest.raises(RuntimeError):
        coll.foundRemote('alpha.jpg', 'h2')

def test_call_globDone_remoteDone_on_new_after_done():
    coll = SyncedFileCollection()
    coll.globDone()
    coll.remoteDone()
    coll.foundFile('beta.csv')
    f = coll.files['beta.csv']
    assert f.globbed
    assert f.remoted