import os
import sqlite3
import pytest
import sqlitedict

def test_readonly_flag(tmp_path):
    db_file = str(tmp_path / "ro.sqlite")
    d = sqlitedict.SqliteDict(db_file)
    d['k'] = 'val'
    d.commit()
    d.close()

    d2 = sqlitedict.SqliteDict(db_file, flag='r')
    assert d2['k'] == 'val'
    with pytest.raises(RuntimeError):
        d2['set_fail'] = 123
    d2.close()

def test_itervalues_and_iteritems(tmp_path):
    db_file = str(tmp_path / "itervals.sqlite")
    d = sqlitedict.SqliteDict(db_file)
    d['a'] = 1
    d['b'] = 2
    d['c'] = 3
    d.commit()
    assert set(d.itervalues()) == {1, 2, 3}
    assert set(k for k, v in d.iteritems()) == {'a', 'b', 'c'}
    d.close()

def test_context_manager(tmp_path):
    db_file = str(tmp_path / "ctx.sqlite")
    with sqlitedict.SqliteDict(db_file) as d:
        d['hello'] = 'world'
        d.commit()
        assert d['hello'] == 'world'
    # After exiting context, connection must be closed
    with pytest.raises(AttributeError):
        d['goodbye'] = 'nope'

def test_keys_values_items(tmp_path):
    db_file = str(tmp_path / "kv.sqlite")
    d = sqlitedict.SqliteDict(db_file)
    pairs = {'abc': 1, 'def': 2}
    for k, v in pairs.items():
        d[k] = v
    d.commit()
    assert set(d.keys()) == set(pairs.keys())
    assert set(d.values()) == set(pairs.values())
    assert set(d.items()) == set(pairs.items())
    d.close()