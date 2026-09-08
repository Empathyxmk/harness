import pytest
import os
import sqlitedict

def test_named_db_branch(tmp_path):
    db_file = tmp_path / "named_db.sqlite"
    d1 = sqlitedict.SqliteDict(str(db_file), tablename="table1")
    d2 = sqlitedict.SqliteDict(str(db_file), tablename="table2")
    d1['a'] = 1
    d2['b'] = 2
    d1.commit()
    d2.commit()
    assert 'a' in d1
    assert 'b' in d2
    d1.close()
    d2.close()

def test_flag_autocommit(tmp_path):
    db_file = tmp_path / "auto.sqlite"
    d = sqlitedict.SqliteDict(str(db_file), autocommit=True)
    d['x'] = 1
    d['y'] = 2
    # Should persist without call to commit
    d2 = sqlitedict.SqliteDict(str(db_file))
    assert d2['x'] == 1
    assert d2['y'] == 2
    d.close()
    d2.close()

def test_flag_encode_key(tmp_path):
    db_file = tmp_path / "encode.sqlite"
    d = sqlitedict.SqliteDict(
        str(db_file),
        encode_key=lambda x: str(x).upper().encode("utf-8"),
        decode_key=lambda x: x.decode("utf-8").lower()
    )
    d["foo"] = "bar"
    d.commit()
    # Correct assertion: decode_key ensures 'foo' is returned
    keys = list(d.keys())
    assert keys == ["foo"]
    d.close()

def test_flag_decode_key(tmp_path):
    db_file = tmp_path / "decode.sqlite"
    d = sqlitedict.SqliteDict(str(db_file),
                              encode_key=lambda x: ("a" + x).encode("utf-8"),
                              decode_key=lambda x: x.decode("utf-8")[1:])
    d["k"] = 11
    d.commit()
    assert "k" in d
    d.close()

def test_flag_tablename_collision(tmp_path):
    db_file = tmp_path / "clash.sqlite"
    d1 = sqlitedict.SqliteDict(str(db_file), tablename="t")
    d2 = sqlitedict.SqliteDict(str(db_file), tablename="t")
    d1['a'] = 1
    d1.commit()
    assert d2.get('a') == 1
    d1.close()
    d2.close()

def test_error_on_closed(tmp_path):
    db_file = tmp_path / "closed.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    d['a'] = 5
    d.close()
    # Should raise AttributeError, not ValueError
    with pytest.raises(AttributeError):
        d['b'] = 6
    with pytest.raises(AttributeError):
        _ = d['a']

def test_in_operator_with_missing_key(tmp_path):
    db_file = tmp_path / "contain.sqlite"
    d = sqlitedict.SqliteDict(str(db_file))
    assert 'zz' not in d
    d.close()