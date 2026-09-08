import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from convert_excel_to_json import convert_excel_to_json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_XLSX = os.path.abspath(os.path.join(THIS_DIR, '../tests/test-data-2.xlsx'))

def test_throw_on_invalid_config_json():
    with pytest.raises(SyntaxError):
        convert_excel_to_json("{foo: true notvalid}")

def test_custom_header_rows_skips_headers():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'header': {'rows': 1}})
    ws = list(result)[0]
    assert all('Name' not in row.values() for row in result[ws])

def test_header_rowtokeys():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'header': {'rowToKeys': 2}})
    assert isinstance(result, dict)

def test_empty_for_missing_sheet():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'sheets': [{'name': 'NO_SHEET'}]})
    assert result['NO_SHEET'] == []

def test_support_source_as_buffer():
    with open(TEST_XLSX, "rb") as f:
        buf = f.read()
    result = convert_excel_to_json({'source': buf})
    assert len(result.keys()) > 0

def test_column_to_key_blank_skips():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'columnToKey': {'B': ""}})
    ws = list(result)[0]
    assert all('' not in row for row in result[ws])

def test_skip_columns_not_in_mapping():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'columnToKey': {'Y': 'notpresent'}})
    ws = list(result)[0]
    assert all(set(row.keys()).issubset(['notpresent']) for row in result[ws])

def test_work_with_mixed_sheets_types():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'sheets': ['Data', {'name': 'Summary'}]})
    assert 'Data' in result or 'Summary' in result

def test_support_sheets_number_of_sheets():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'sheets': {'numberOfSheetsToGet': 2}})
    assert len(result.keys()) in (1,2)

def test_not_throw_if_range_excludes_all():
    result = convert_excel_to_json({'sourceFile': TEST_XLSX, 'range': 'Q10:Q20'})
    ws = list(result)[0]
    assert isinstance(result[ws], list)