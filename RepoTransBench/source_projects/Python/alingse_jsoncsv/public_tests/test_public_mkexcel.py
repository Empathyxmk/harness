import io
import os
import tempfile
import json
import pytest

from jsoncsv import dumptool

def test_dumpcsv_and_patch_value(tmp_path):
    # Test values different than original: change keys and values
    objs = [
        {"alpha": 7, "omega": 21},
        {"alpha": 0, "omega": None},  # None -> empty string
        {"alpha": {}, "omega": []},
    ]
    # Write to a temp file
    out_path = tmp_path / "out_pub.csv"
    with out_path.open("wb") as fout:
        d = dumptool.DumpCSV(
            io.StringIO('\n'.join(json.dumps(o) for o in objs) + '\n'),
            fout,
        )
        d.dump()
    # Now read back for presence of headers
    content = out_path.read_text(encoding="utf-8")
    for col in ("alpha", "omega"):
        assert col in content
    assert ',,' not in content  # consecutive empty columns should not appear

def test_dumpxls_and_patch_value(tmp_path):
    objs = [
        {"theta": 3, "sigma": 5},
        {"theta": 0, "sigma": {}},  # {} patched
        {"theta": None, "sigma": 2},
    ]
    out_path = tmp_path / "pub_output.xls"
    with out_path.open("wb") as fout:
        d = dumptool.DumpXLS(
            io.StringIO('\n'.join(json.dumps(o) for o in objs) + '\n'),
            fout,
        )
        d.dump()
    # Check file was written non-empty
    assert out_path.stat().st_size > 0

def test_read_headers_reads_all(tmp_path):
    # Test with different keys
    lines = [
        json.dumps({"one": 1, "two": 2}),
        json.dumps({"two": 3, "three": 4}),
    ]
    with io.StringIO('\n'.join(lines) + '\n') as fin:
        headers, datas = dumptool.ReadHeadersMixin.load_headers(fin)
    assert set(headers) >= {"one", "two", "three"}
    assert len(datas) == 2

def test_dumpcsv_patch_empty_struct(tmp_path):
    # Test csv output with list in value, should be patched to ''
    objs = [
        {"foo": [], "bar": 1},
        {"foo": [1, 2], "bar": 2},
    ]
    out_path = tmp_path / "test_pub_patch.csv"
    with out_path.open("wb") as fout:
        d = dumptool.DumpCSV(
            io.StringIO('\n'.join(json.dumps(o) for o in objs) + '\n'),
            fout,
        )
        d.dump()
    content = out_path.read_text(encoding="utf-8")
    assert "foo" in content and "bar" in content