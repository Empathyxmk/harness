import pytest
from cppstddb.test_suite import test_all

def test_sqlite_public():
    from cppstddb.sqlite import database
    uri = "file://publictestdb_unique.sqlite"
    test_all(database, uri)