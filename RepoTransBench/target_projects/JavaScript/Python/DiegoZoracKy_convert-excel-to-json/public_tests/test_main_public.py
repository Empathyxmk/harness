import os
import sys
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from convert_excel_to_json import convert_excel_to_json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_SOURCE_FILE = os.path.abspath(os.path.join(THIS_DIR, '../tests/test-data-2.xlsx'))
with open(PUBLIC_SOURCE_FILE, "rb") as f:
    PUBLIC_SOURCE_BUFFER = f.read()

def _basic_public(param):
    result = convert_excel_to_json(param)
    assert isinstance(result, dict)
    assert len(result) >= 1
    ws = list(result)[0]
    assert isinstance(result[ws], list)
    assert len(result[ws]) > 0

def test_throw_if_config_missing_sourcefile_or_source():
    with pytest.raises(Exception):
        convert_excel_to_json({'sheets': []})

def test_simple_object_literal():
    _basic_public({'sourceFile': PUBLIC_SOURCE_FILE})

def test_simple_json_string():
    _basic_public(json.dumps({'sourceFile': PUBLIC_SOURCE_FILE}))

def test_simple_buffer_source():
    _basic_public({'source': PUBLIC_SOURCE_BUFFER})

def test_sheets_config_data_and_summary():
    r = convert_excel_to_json({'sourceFile': PUBLIC_SOURCE_FILE, 'sheets': ['Data', {'name':'Summary'}]})
    assert isinstance(r, dict)
    assert len(r) == 2
    assert 'Data' in r and 'Summary' in r
    assert isinstance(r['Data'], list)
    assert len(r['Data']) >= 3
    assert 'A' in r['Data'][0]
    assert isinstance(r['Summary'], list)
    assert len(r['Summary']) >= 1
    assert 'A' in r['Summary'][0]

def test_get_only_summary_sheet():
    r = convert_excel_to_json({'sourceFile': PUBLIC_SOURCE_FILE, 'sheets': ['Summary']})
    assert isinstance(r, dict)
    assert len(r) == 1
    assert r.get('Data', None) is None or 'Data' not in r or r['Data'] is None
    assert 'Summary' in r
    summary = r['Summary']
    assert len(summary) >= 1
    assert 'A' in summary[0]