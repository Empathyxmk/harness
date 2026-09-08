import sys
import os

# Ensure we can import sqlitedict for public test runs regardless of working dir
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlitedict
import tempfile
import pytest

def test_public_small_and_large_keys_and_values():
    with sqlitedict.SqliteDict(':memory:') as d:
        # Trivial case
        d[""] = "z"
        assert d[""] == "z"

        # Long key and value
        key = "k" * 2000
        val = "v" * 8000
        d[key] = val
        assert d[key] == val

def test_public_large_number_of_keys():
    with sqlitedict.SqliteDict(':memory:') as d:
        # Fewer than original, but distinct for public test
        N = 2117
        for i in range(N):
            d[str(i)] = i * 7
        for i in range(N):
            assert d[str(i)] == i * 7

def test_public_numeric_value_types():
    with sqlitedict.SqliteDict(':memory:') as d:
        d['n1'] = 1.5
        d['n2'] = -42
        d['n3'] = 2**30
        d['n4'] = 0
        assert d['n1'] == 1.5
        assert d['n2'] == -42
        assert d['n3'] == 2**30
        assert d['n4'] == 0

def test_public_unicode_and_binary():
    with sqlitedict.SqliteDict(':memory:') as d:
        k = "unicø∂e"
        v = "välues💡"
        d[k] = v
        assert d[k] == v
        bin_k = b'\xff\xfe\xfd'  # Should work as a key
        bin_v = b"\x00\x01\x02"
        d[bin_k] = bin_v
        assert d[bin_k] == bin_v

def test_public_temp_db_persistence():
    tf = tempfile.NamedTemporaryFile(delete=False)
    dbfile = tf.name
    tf.close()
    d = sqlitedict.SqliteDict(dbfile, autocommit=True)
    d['foo'] = 'bar'
    d['baz'] = [1,2,3]
    d.close()
    d2 = sqlitedict.SqliteDict(dbfile)
    assert d2['foo'] == 'bar'
    assert d2['baz'] == [1,2,3]
    d2.close()
    os.unlink(dbfile)