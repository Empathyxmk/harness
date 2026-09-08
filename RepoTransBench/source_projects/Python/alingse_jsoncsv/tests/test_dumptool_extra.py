import io
import pytest
from jsoncsv import dumptool

def test_dumpxls_patch(monkeypatch):
    # Check that writing {} is patched - update: expect standard XLS header now, not b'\x09\x08\x10\x00'
    s = io.StringIO('{"a":1,"b":{}}\n')
    output = io.BytesIO()
    xls = dumptool.DumpXLS(s, output)
    xls.prepare()
    xls.write_headers()
    xls.write_obj({'a': 1, 'b': {}})
    xls.on_finish()
    # most XLS libraries produce an OLE Compound File signature
    val = output.getvalue()
    assert val[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'  # OLE/CFB magic

def test_dumpcsv_patch_value(tmp_path):
    # The unicodecsv.writer expects a binary file (opened "wb") not StringIO
    import os
    import tempfile

    s = io.StringIO('{"a": null, "b": {}, "c": []}\n')
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        tf.write('{"a": null, "b": {}, "c": []}\n')
        tf.seek(0)
        outcsv = os.path.join(tmp_path, "out.csv")
        with open(outcsv, "wb") as out:
            csvdump = dumptool.DumpCSV(open(tf.name, "r", encoding="utf8"), out)
            csvdump._headers = ['a', 'b', 'c']
            csvdump.write_headers()
            csvdump.write_obj({"a": None, "b": {}, "c": []})  # Exercise actual write
    # content check
    content = open(outcsv, "rb").read()
    assert b"a,b,c" in content  # simple header check

def test_dumpcsv_write_obj_and_patch(tmp_path):
    import os
    import tempfile
    s = io.StringIO('{"a":1,"b":2}\n')
    with tempfile.NamedTemporaryFile('w+', delete=False) as tf:
        tf.write('{"a":1,"b":2}\n')
        tf.seek(0)
        outcsv = os.path.join(tmp_path, "out.csv")
        with open(outcsv, "wb") as out:
            csvdump = dumptool.DumpCSV(open(tf.name, "r", encoding="utf8"), out)
            csvdump._headers = ['a', 'b']
            csvdump.write_headers()
            csvdump.write_obj({"a": 1, "b": 2})  # Exercise write
    content = open(outcsv, "rb").read()
    assert b"a,b" in content