import pytest

class StorageService:
    def init(self):
        raise NotImplementedError
    def store(self, f, s):
        raise NotImplementedError
    def loadAll(self):
        raise NotImplementedError
    def load(self, file):
        raise NotImplementedError
    def loadAsResource(self, file):
        raise NotImplementedError
    def deleteAll(self):
        raise NotImplementedError

def test_dummy_interface_implementation_different_data():
    # Provide a different return for store, different input for load
    class MyStorageService(StorageService):
        def init(self):
            pass
        def store(self, f, s):
            return "public-ok"
        def loadAll(self):
            # return an iterator with one Path
            from pathlib import Path
            return iter([Path("publicfile")])
        def load(self, file):
            from pathlib import Path
            return Path("publicfile")
        def loadAsResource(self, file):
            return None
        def deleteAll(self):
            pass
    s = MyStorageService()
    assert s is not None
    s.init()
    assert s.store(None, "public") == "public-ok"
    lAll = s.loadAll()
    assert next(lAll, None) is not None
    from pathlib import Path
    assert s.load("public") == Path("publicfile")
    assert s.loadAsResource("public") is None
    s.deleteAll()