import os
import pytest
import sqlitedict

def test_sqlitedict_autocommit(tmp_path):
    db_file = tmp_path / "auto.sqlite"
    d = sqlitedict.SqliteDict(str(db_file), autocommit=True)
    d['foo'] = 42
    d['bar'] = 123
    d.close()
    d = sqlitedict.SqliteDict(str(db_file))
    assert d['foo'] == 42
    assert d['bar'] == 123
    d.close()

def test_sqlitedict_flag_r_and_n(tmp_path):
    db_file = tmp_path / "flagr.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['a'] = 1
    d.commit()
    d.close()
    # open in read-only mode
    d = sqlitedict.SqliteDict(str(db_file), flag='r')
    assert d['a'] == 1
    with pytest.raises(Exception):
        d['b'] = 2
    d.close()

    # create new db with flag=n
    n_db = tmp_path / "flagn.sqlite"
    d = sqlitedict.SqliteDict(str(n_db), flag='n')
    d['first'] = 2
    d.commit()
    assert d['first'] == 2
    d.close()

def test_sqlitedict_journal_mode_off(tmp_path):
    db_file = tmp_path / "journal.sqlite"
    d = sqlitedict.SqliteDict(str(db_file), journal_mode="OFF")
    d['x'] = 1
    d.commit()
    d.close()
    d = sqlitedict.SqliteDict(str(db_file), journal_mode="DELETE")
    assert d['x'] == 1
    d.close()

def test_sqlitedict_custom_encode_decode(tmp_path):
    import json
    def encode(obj): return json.dumps(obj).encode("utf8")
    def decode(obj): return json.loads(obj.decode("utf8"))
    db_file = tmp_path / "json.sqlite"
    d = sqlitedict.SqliteDict(str(db_file), encode=encode, decode=decode)
    d['json'] = {'a': 1, 'b': 2}
    assert d['json']['a'] == 1
    d.close()

def test_sqlitedict_outer_stack_false(tmp_path):
    db_file = tmp_path / "outerstack.sqlite"
    d = sqlitedict.SqliteDict(str(db_file), outer_stack=False)
    d['x'] = 1
    d.close()