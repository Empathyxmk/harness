import tempfile
import os
import pytest

class EmbeddedPostgres:
    DEFAULT_DB_NAME = "defaultdb"

class Storage:
    def __init__(self, db_name):
        self._db_dir = tempfile.mkdtemp()
        self._db_name = db_name

    def dbDir(self):
        class DbDir:
            def __init__(self, path):
                self._p = path
            def exists(self):
                return os.path.exists(self._p)
            def getPath(self):
                return self._p
        return DbDir(self._db_dir)

def test_it_should_allow_to_make_two_storage_with_one_database_name():
    storage0 = Storage(EmbeddedPostgres.DEFAULT_DB_NAME)
    assert storage0.dbDir().exists()
    storage1 = Storage(EmbeddedPostgres.DEFAULT_DB_NAME)
    assert storage1.dbDir().exists()
    assert storage0.dbDir().getPath() != storage1.dbDir().getPath()