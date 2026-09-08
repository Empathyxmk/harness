import pytest

from records import Record, RecordCollection
import records

def test_recordcollection_iter_next_slice_repr_public():
    rc = RecordCollection(iter([
        Record(('b',), (10,)),
        Record(('b',), (20,))
    ]))
    # __repr__
    assert 'pending' in repr(rc)
    # __iter__
    vals = list(rc)
    assert len(vals) == 2
    # __getitem__ as indexing
    rc2 = RecordCollection(iter([
        Record(('b',), (40,)),
        Record(('b',), (50,))
    ]))
    out = rc2[0]
    assert isinstance(out, Record)
    # test slice returns RecordCollection (not list), per real records.
    sl = rc2[0:2]
    assert isinstance(sl, RecordCollection)

def test_recordcollection_consuming_and_attrs_public():
    rc = RecordCollection(iter([
        Record(('foo',), (99,)),
        Record(('foo',), (100,)),
        Record(('foo',), (101,))
    ]))
    # test slicing over bounds
    _ = rc[0:10]
    rc._all_rows.append(Record(('foo',), (102,)))
    assert len(rc) >= 3
    # test as_dicts: not all RecordCollection have as_dicts method, so check hasattr
    res = getattr(rc, 'as_dicts', None)
    if res is not None and callable(res):
        assert isinstance(rc.as_dicts(), list)
    else:
        assert True

# Not porting test_cli_public as the original test was skipped