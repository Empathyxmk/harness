import os
import tempfile
import pytest
import sqlitedict

@pytest.fixture
def temp_db_file():
    fd, path = tempfile.mkstemp(suffix='.sqlite')
    os.close(fd)
    try:
        yield path
    finally:
        try:
            os.remove(path)
        except Exception:
            pass

def test_sqlitedict_set_get_del_len_clear(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    d['a'] = 1
    d['b'] = 2
    assert d['a'] == 1
    assert d['b'] == 2
    assert len(d) == 2
    del d['a']
    assert 'a' not in d
    assert len(d) == 1
    d.clear()
    assert len(d) == 0
    d.close()

def test_sqlitedict_context_manager(temp_db_file):
    with sqlitedict.SqliteDict(temp_db_file) as d:
        d['foo'] = 'bar'
        assert d['foo'] == 'bar'
    # It should be closed after context

def test_sqlitedict_commit_remove(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    d['a'] = 10
    d.commit()
    d['b'] = 20
    d.clear()
    assert len(d) == 0
    d.close()

def test_sqlitedict_iter_methods(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    for i in range(5):
        d[str(i)] = i
    keys = set(d.keys())
    assert keys == set(str(i) for i in range(5))
    values = set(d.values())
    assert values == set(range(5))
    items = set(d.items())
    assert items == set((str(i), i) for i in range(5))
    d.close()

def test_sqlitedict_get_default(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    assert d.get('nonexistent') is None
    assert d.get('nonexistent', 123) == 123
    d.close()

def test_sqlitedict_update(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    d.update({'x': 1, 'y': 2})
    assert d['x'] == 1
    assert d['y'] == 2
    d.close()

def test_sqlitedict_contains(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    d['present'] = 1
    assert 'present' in d
    assert 'missing' not in d
    d.close()

def test_sqlitedict_repr(temp_db_file):
    d = sqlitedict.SqliteDict(temp_db_file)
    s = repr(d)
    assert 'SqliteDict' in s
    d.close()

def test_sqlitedict_non_existing_file():
    # Should create file if not exists
    with tempfile.NamedTemporaryFile(suffix='.sqlite', delete=True) as tf:
        path = tf.name
    d = sqlitedict.SqliteDict(path)
    d['key'] = 'val'
    d.commit()
    d.close()
    assert os.path.exists(path)
    os.remove(path)