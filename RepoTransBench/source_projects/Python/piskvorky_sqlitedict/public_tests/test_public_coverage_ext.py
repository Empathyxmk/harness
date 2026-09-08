import sys
import os

# Ensure we can import sqlitedict for public test runs regardless of working dir
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlitedict
import tempfile
import pytest

def test_public_open_close_reopen():
    "Verify that a db can be opened, closed, and reopened, with data retained."
    tf = tempfile.NamedTemporaryFile(delete=False)
    dbfile = tf.name
    tf.close()
    d = sqlitedict.SqliteDict(dbfile, autocommit=True)
    d["foo"] = "bar"
    d["baz"] = 45
    d.close()

    d2 = sqlitedict.SqliteDict(dbfile, autocommit=True)
    assert d2["foo"] == "bar"
    assert d2["baz"] == 45
    d2.close()
    os.unlink(dbfile)

def test_public_table_separation():
    "Verify different tables in same DB file are isolated."
    tf = tempfile.NamedTemporaryFile(delete=False)
    dbfile = tf.name
    tf.close()
    d1 = sqlitedict.SqliteDict(dbfile, tablename="A", autocommit=True)
    d2 = sqlitedict.SqliteDict(dbfile, tablename="B", autocommit=True)
    d1['x1'] = "fooA"
    d2['x1'] = "fooB"
    d1.close()
    d2.close()

    d1b = sqlitedict.SqliteDict(dbfile, tablename="A")
    d2b = sqlitedict.SqliteDict(dbfile, tablename="B")
    assert d1b['x1'] == "fooA"
    assert d2b['x1'] == "fooB"
    d1b.close()
    d2b.close()
    os.unlink(dbfile)

@pytest.mark.parametrize('autocommit', [True, False])
def test_public_basic_set_get_del(autocommit):
    "Set, get, and delete an item; ensure it behaves."
    with sqlitedict.SqliteDict(':memory:', autocommit=autocommit) as d:
        d['xyz'] = 678
        assert d['xyz'] == 678
        del d['xyz']
        assert 'xyz' not in d

def test_public_len_and_clear():
    "Test len and clear on dict with some elements"
    with sqlitedict.SqliteDict(':memory:') as d:
        vals = list(range(10, 16))
        for idx, k in enumerate(['a','b','c','d','e','f']):
            d[k] = vals[idx]
        assert len(d) == 6
        d.clear()
        assert len(d) == 0

def test_public_contains_pop_and_keys():
    "Check contains, pop, and that keys() returns expected set"
    with sqlitedict.SqliteDict(':memory:') as d:
        d["k1"] = 333
        d["k2"] = 444
        d["k3"] = 555
        assert "k1" in d
        assert d.pop("k2") == 444
        keys = set(d.keys())
        assert keys == {"k1","k3"}