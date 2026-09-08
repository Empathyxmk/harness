import io
import json
import pytest

from jsoncsv.dumptool import DumpCSV, DumpXLS

def test_csv_with_extra_keys(tmp_path):
    # see that csv handles extra keys in second row
    data = [
        {"colA": "test1", "colB": 7},
        {"colA": "test2", "colC": 8},
    ]
    out_file = tmp_path / "extra_pub.csv"
    fin = io.StringIO('\n'.join(json.dumps(d) for d in data))
    with out_file.open("wb") as fout:
        d = DumpCSV(fin, fout)
        d.dump()
    content = out_file.read_text("utf-8")
    assert "colA" in content and "colB" in content and "colC" in content

def test_xls_with_missing_keys(tmp_path):
    data = [
        {"aa": 2, "bb": 4},
        {"aa": 3},  # bb missing
    ]
    out_file = tmp_path / "missing_pub.xls"
    fin = io.StringIO('\n'.join(json.dumps(d) for d in data))
    with out_file.open("wb") as fout:
        d = DumpXLS(fin, fout)
        d.dump()
    assert out_file.stat().st_size > 0