import io
import json
import pytest

from jsoncsv.dumptool import ReadHeadersMixin, DumpCSV, DumpXLS, DumpExcel

def test_read_headers_varied(tmp_path):
    records = [
        {"fruit": "apple", "amount": 5},
        {"fruit": "banana", "price": 3.1},
        {"price": 2, "color": "yellow"},
    ]
    f = io.StringIO('\n'.join(json.dumps(obj) for obj in records))
    headers, datas = ReadHeadersMixin.load_headers(f)
    # Should at least get superset of all keys from all records
    for key in ("fruit", "amount", "price", "color"):
        assert key in headers
    assert len(datas) == 3

def test_dumpcsv_patch_types(tmp_path):
    objs = [
        {"x": {}, "y": 1},
        {"x": [], "y": 2},
        {"x": None, "y": 3},
    ]
    out_path = tmp_path / "patchpub.csv"
    with out_path.open("wb") as fout:
        d = DumpCSV(io.StringIO('\n'.join(json.dumps(o) for o in objs) + '\n'), fout)
        d.dump()
    contents = out_path.read_text(encoding="utf-8")
    assert "x" in contents and "y" in contents

def test_dumpxls_patch_types(tmp_path):
    objs = [
        {"a": 10, "b": {}},
        {"a": None, "b": 5},
    ]
    out_path = tmp_path / "patchpub.xls"
    with out_path.open("wb") as fout:
        d = DumpXLS(io.StringIO('\n'.join(json.dumps(o) for o in objs) + '\n'), fout)
        d.dump()
    assert out_path.stat().st_size > 0

def test_dumpexcel_wrongtype(tmp_path):
    class NotDumpExcel: pass
    with pytest.raises(ValueError):
        ReadHeadersMixin.load_headers(io.StringIO('{"foo":1}\n'))
        # This line above doesn't raise, so check manually for dump_excel
        io_obj = io.StringIO('{"foo":1}\n')
        DumpExcel.init = lambda self, fin, fout, **kw: None
        with pytest.raises(ValueError):
            from jsoncsv import dumptool
            dumptool.dump_excel(io_obj, io.BytesIO(), NotDumpExcel)