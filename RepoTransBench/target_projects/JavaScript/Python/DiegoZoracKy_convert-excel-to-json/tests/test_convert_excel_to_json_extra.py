import os
import sys
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from convert_excel_to_json import convert_excel_to_json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_XLSX = os.path.join(THIS_DIR, "test-data.xlsx")

def test_throw_on_invalid_json_config():
    with pytest.raises(SyntaxError):
        convert_excel_to_json("{notjson: true,}")

def test_custom_header_rows_skips_headers():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'header': {'rows': 2}})
    ws = list(result.keys())[0]
    # All rows must not contain the header 'id'
    assert all('id' not in row.values() for row in result[ws])

def test_header_rowtokeys_given_template_keying():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'header': {'rowToKeys': 1}})
    assert isinstance(result, dict)

def test_empty_array_for_missing_sheet():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'sheets': [{'name': 'INVALIDSHEETNAME'}]})
    assert result['INVALIDSHEETNAME'] == []

def test_support_source_as_buffer():
    with open(TEST_XLSX, "rb") as f:
        buf = f.read()
    result = convert_excel_to_json({'source': buf})
    assert len(result.keys()) > 0

def test_accept_column_to_key_blank_and_skip():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'columnToKey': {'A': ""}})
    ws = list(result)[0]
    assert all('' not in row for row in result[ws])

def test_skip_columns_not_in_column_to_key():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'columnToKey': {'X': 'notused'}})
    ws = list(result)[0]
    # Only 'notused' or empty
    for row in result[ws]:
        assert all(k == 'notused' for k in row.keys()) or not row

def test_work_with_sheets_mixed_types():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'sheets': ['sheet1', {'name':'sheet2'}]})
    assert 'sheet1' in result and 'sheet2' in result

def test_support_sheets_number_of_sheets():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'sheets': {'numberOfSheetsToGet': 1}})
    assert len(result.keys()) == 1

def test_not_throw_if_range_excludes_all():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'range': 'Z1:Z2'})
    ws = list(result.keys())[0]
    assert isinstance(result[ws], list)