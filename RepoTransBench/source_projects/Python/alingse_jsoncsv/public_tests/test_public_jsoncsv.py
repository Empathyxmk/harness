import io
import json
import csv
import tempfile
import shutil
import os
import pytest

from jsoncsv import dumptool, jsontool

def test_public_simple_jsoncsv_csv(tmp_path):
    # Create simple objects
    data = [
        {"book": "A Tale", "price": 12},
        {"book": "Enders Game", "price": 25},
    ]
    inpath = tmp_path / "in_pub.csvjson"
    outpath = tmp_path / "out_pub.csv"
    inpath.write_text('\n'.join(json.dumps(d) for d in data))
    with inpath.open("r", encoding="utf-8") as fin, outpath.open("wb") as fout:
        d = dumptool.DumpCSV(fin, fout)
        d.dump()
    content = outpath.read_text(encoding="utf-8")
    assert "book" in content and "price" in content

def test_public_simple_jsoncsv_xls(tmp_path):
    data = [
        {"city": "London", "pop": 8},
        {"city": "Paris", "pop": 6},
    ]
    inpath = tmp_path / "in_pub.xlsjson"
    outpath = tmp_path / "out_pub.xls"
    inpath.write_text('\n'.join(json.dumps(d) for d in data))
    with inpath.open("r", encoding="utf-8") as fin, outpath.open("wb") as fout:
        d = dumptool.DumpXLS(fin, fout)
        d.dump()
    assert outpath.stat().st_size > 0

def test_public_patch_value_different_types():
    d = dumptool.DumpCSV(io.StringIO(''), io.BytesIO())
    assert d.patch_value(None) == ""
    assert d.patch_value({}) == ""
    assert d.patch_value([]) == ""
    assert d.patch_value("something") == "something"
    assert d.patch_value(10) == 10