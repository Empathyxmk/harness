import os
import pytest
import sqlite3
import sqlitedict

def test_sqlitedict_iteration_and_clear(tmp_path):
    db_file = tmp_path / "iterclear.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    for i in range(10):
        d[str(i)] = i
    d.commit()
    keys = list(d.keys())
    items = list(d.items())
    values = list(d.values())
    assert set(keys) == set(str(i) for i in range(10))
    assert len(items) == 10
    assert all(v in range(10) for v in values)
    d.clear()
    assert list(d.keys()) == []
    d.close()

def test_sqlitedict_pop_and_update(tmp_path):
    db_file = tmp_path / "popupdate.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['a'] = 10
    d['b'] = 20
    d.commit()
    v = d.pop('a')
    assert v == 10
    assert 'a' not in d
    d.update({'c': 30, 'd': 40})
    assert d['c'] == 30 and d['d'] == 40
    d.close()

def test_sqlitedict_delitem(tmp_path):
    db_file = tmp_path / "delitem.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['x'] = 5
    d.commit()
    del d['x']
    with pytest.raises(KeyError):
        _ = d['x']
    d.close()

def test_sqlitedict_len_and_contains(tmp_path):
    db_file = tmp_path / "lencontains.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['k1'] = 11
    d['k2'] = 22
    d.commit()
    assert len(d) == 2
    assert 'k1' in d
    assert 'notkey' not in d
    d.close()

def test_sqlitedict_repr(tmp_path):
    db_file = tmp_path / "repr.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['r'] = "v"
    rep = repr(d)
    assert "sqlitedict" in rep
    d.close()

def test_sqlitedict_context_manager(tmp_path):
    db_file = tmp_path / "ctx.sqlite"
    with sqlitedict.SqliteDict(str(db_file)) as d:
        d['foo'] = 'bar'
        d.commit()
    with sqlitedict.SqliteDict(str(db_file)) as d:
        assert d['foo'] == 'bar'

def test_sqlitedict_from_dict(tmp_path):
    db_file = tmp_path / "fromdict.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d.update({'one': 1, 'two': 2})
    d.commit()
    nd = dict(d)
    assert nd['one'] == 1 and nd['two'] == 2
    d.close()

def test_sqlitedict_close_twice(tmp_path):
    db_file = tmp_path / "close2.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['foo'] = 42
    d.close()
    d.close()  # closing twice should not fail