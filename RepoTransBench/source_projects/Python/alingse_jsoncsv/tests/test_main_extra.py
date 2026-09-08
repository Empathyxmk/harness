from click.testing import CliRunner
from jsoncsv import main
import os

def test_mkexcel_csv_and_xls(tmp_path):
    runner = CliRunner()
    infile = tmp_path / "in.json"
    infile.write_text('{"a":1}\n{"a":2}\n')
    outcsv = tmp_path / "out.csv"
    outxls = tmp_path / "out.xls"
    # CSV file
    result_csv = runner.invoke(main.mkexcel, ["--type", "csv", str(infile), str(outcsv)])
    assert result_csv.exit_code == 0
    assert outcsv.read_bytes().startswith(b"a")
    # XLS file
    result_xls = runner.invoke(main.mkexcel, ["--type", "xls", str(infile), str(outxls)])
    assert result_xls.exit_code == 0
    # fix: expect proper OLE magic for .xls files, not b'\x09\x08\x10\x00'
    assert outxls.read_bytes()[:8] == b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'