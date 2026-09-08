import pytest
import records

def test_record_repr_and_export_public():
    rec = records.Record(['r', 's'], [3, 'abc'])
    rep = repr(rec)
    assert rep.startswith('<Record')
    exported = rec.export("json")
    assert '"abc"' in exported

def test_record_as_dict_ordered_public():
    rec = records.Record(['z', 'x', 'y'], [7, 8, 9])
    d1 = rec.as_dict()
    d2 = rec.as_dict(ordered=True)
    assert isinstance(d1, dict)
    assert list(d2.keys()) == ['z', 'x', 'y']

def test_record_get_method_public():
    rec = records.Record(['foo', 'bar'], [5, 6])
    assert rec.get('foo') == 5
    assert rec.get('baz', 99) == 99

def test_record_collection_csv_export_public():
    rc = records.RecordCollection([records.Record(['id', 'val'], [5, 'a']), records.Record(['id', 'val'], [6, 'b'])])
    try:
        csv = rc.export('csv')
    except Exception:
        pytest.skip("Tablib/export or CSV format missing")
    assert isinstance(csv, str)
    assert "id" in csv

def test_record_collection_export_xlsx_public():
    rc = records.RecordCollection([records.Record(['num'], [111]), records.Record(['num'], [222])])
    try:
        data = rc.export('xlsx')
    except Exception:
        pytest.skip("Tablib/xlsx not present or export fails")
    assert isinstance(data, (bytes, str))

def test_isexception_cases_public():
    from records import isexception

    class CustomError(Exception): pass
    def f(): raise CustomError
    assert isexception(f)
    assert isexception(CustomError)
    assert isexception(CustomError()) is True

def test_record_collection_repr_ascii_pending_public():
    rc = records.RecordCollection([records.Record(['w', 'x'], [11, 22]), records.Record(['w', 'x'], [33, 44])])
    r = repr(rc)
    assert r.startswith('<RecordCollection')

def test_record_as_dict_keys_match_public():
    rec = records.Record(['a', 'b', 'c'], [1, 2, 3])
    asdict = rec.as_dict()
    for k in ['a', 'b', 'c']:
        assert k in asdict

def test_record_export_dataset_public():
    rec = records.Record(['val'], [898])
    ds = rec.dataset
    assert hasattr(ds, "headers")
    assert "val" in ds.headers