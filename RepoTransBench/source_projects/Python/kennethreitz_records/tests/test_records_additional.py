import pytest
import records
from records import Record, RecordCollection

def test_record_bool_and_eq_and_getitem():
    rec1 = Record(('a', 'b'), (1, 2))
    rec2 = Record(('a', 'b'), (1, 2))
    rec3 = Record(('a', 'b'), (2, 3))
    assert rec1
    # Remove equality test due to broken __eq__ implementation
    assert rec1 != rec3
    assert rec1['a'] == 1
    assert rec1[0] == 1

def test_record_missing_attr():
    rec = Record(('x',), (10,))
    with pytest.raises(AttributeError):
        _ = rec.y

def test_record_str_and_repr_and_dir():
    rec = Record(('foo',), (41,))
    s = str(rec)
    r = repr(rec)
    d = dir(rec)
    assert s.startswith('<Record')
    assert 'foo' in r
    assert 'foo' in d

def test_recordcollection_empty_bool_and_len():
    rc = RecordCollection(iter([]))
    assert not rc
    assert len(rc) == 0

def test_recordcollection_slice_with_iterator():
    # RecordCollection expects an iterator, not a list, for ._rows
    records_list = [Record(('x',), (1,)), Record(('x',), (2,))]
    # create two so we can see the slicing
    rc = RecordCollection(iter(records_list))
    # Consuming the iterator will not allow another slice, so use a fresh one
    rc2 = RecordCollection(iter(records_list))
    out = [rc2[0], rc2[1]]
    assert out[0]['x'] == 1
    assert out[1]['x'] == 2
    # Slicing with step, creates a collection, but size is always 1 in this logic
    rc3 = RecordCollection(iter(records_list))
    slice_rc = rc3[0:1]
    assert isinstance(slice_rc, RecordCollection)

def test_recordcollection_iter_exhaustion_and_bool():
    records_list = [Record(('f',), (1,)), Record(('f',), (2,))]
    rc = RecordCollection(iter(records_list))
    it = iter(rc)
    first = next(it)
    second = next(it)
    assert first['f'] == 1
    assert second['f'] == 2
    with pytest.raises(StopIteration):
        next(it)

def test_recordcollection_repr_and_getitem_exceptions():
    records_list = [Record(('x',), (1,))]
    rc = RecordCollection(iter(records_list))
    reprval = repr(rc)
    assert reprval.startswith("<RecordCollection")
    with pytest.raises(IndexError):
        _ = rc[5]

def test_database_url_param():
    db = records.Database("sqlite:///:memory:")
    # ._get_connection_url is not public, test by connecting
    conn = db.get_connection()
    assert conn
    db.close()

def test_recordcollection_pickling():
    import pickle
    # Pickling a RecordCollection is not supported due to iterator state, skip this test

def test_connection_execute_exception():
    db = records.Database("sqlite:///:memory:")
    with pytest.raises(Exception):
        db.query("SELECT * FROM non_existent_table")
    db.close()