import pytest
import sqlitedict

def test_invalid_filename_type():
    # Pass an integer rather than a string/Path
    with pytest.raises(Exception):
        sqlitedict.SqliteDict(12345)

def test_invalid_flag():
    # Pass an invalid flag
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.sqlite') as tf:
        with pytest.raises(RuntimeError):
            sqlitedict.SqliteDict(tf.name, flag='invalid')

def test_closed_dict_operations(tmp_path):
    db = tmp_path / "test.sqlite"
    d = sqlitedict.SqliteDict(str(db))
    d['a'] = 123
    d.close()
    with pytest.raises(Exception):
        d['a'] = 999
    with pytest.raises(Exception):
        _ = d['a']
    with pytest.raises(Exception):
        del d['a']
    with pytest.raises(Exception):
        d.update({'b': 1})
    # The default commit/clear/rollback on closed does NOT always raise Exception (may be silent or idempotent)
    with pytest.raises(Exception):
        _ = list(d.items())

def test_contains_with_closed(tmp_path):
    db = tmp_path / "c.sqlite"
    d = sqlitedict.SqliteDict(str(db))
    d['x'] = 'y'
    d.close()
    with pytest.raises(Exception):
        _ = 'x' in d