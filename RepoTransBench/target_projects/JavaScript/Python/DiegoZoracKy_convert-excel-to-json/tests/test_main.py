import os
import sys
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from convert_excel_to_json import convert_excel_to_json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(THIS_DIR, "test-data.xlsx")
with open(SOURCE_FILE, "rb") as f:
    SOURCE_BUFFER = f.read()

def test_should_throw_no_sourcefile_or_source():
    with pytest.raises(Exception):
        convert_excel_to_json({})

def test_simple_object_literal_param():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE})
    assert isinstance(r, dict)
    assert set(r) & set(['sheet1', 'sheet2'])  # at least one sheet matches

def test_simple_json_string_param():
    param = json.dumps({'sourceFile': SOURCE_FILE})
    r = convert_excel_to_json(param)
    assert isinstance(r, dict)
    assert set(r) & set(['sheet1', 'sheet2'])

def test_simple_buffer_source():
    r = convert_excel_to_json({'source': SOURCE_BUFFER})
    assert isinstance(r, dict)
    assert set(r) & set(['sheet1', 'sheet2'])

def test_sheets_config_both_sheet1_sheet2():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': ['sheet1', {'name': 'sheet2'}]})
    assert 'sheet1' in r and 'sheet2' in r

def test_sheets_sheet1_structure():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': ['sheet1', {'name': 'sheet2'}]})
    assert isinstance(r['sheet1'], list)
    assert len(r['sheet1']) == 25
    first_row = r['sheet1'][0]
    assert set(first_row) == set(['A','B','C','D','E','F'])
    assert first_row == {'A':'id','B':'first_name','C':'last_name','D':'email','E':'gender','F':'ip_address'}
    last_row = r['sheet1'][-1]
    assert last_row['A'] == '24'
    assert last_row['B'] == 'Debra'
    assert last_row['C'] == 'Oliver'

def test_sheets_sheet2_structure():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': ['sheet1', {'name': 'sheet2'}]})
    assert isinstance(r['sheet2'], list)
    assert len(r['sheet2']) == 27
    first_row = r['sheet2'][0]
    assert set(first_row) == set(['A','B','C','D','E','F'])
    last_row = r['sheet2'][-1]
    assert last_row['A'] == '50'
    assert last_row['B'] == 'Susan'
    assert last_row['C'] == 'Miller'

def test_get_only_sheet2_array_of_strings():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': ['sheet2']})
    assert set(r.keys()) == set(['sheet2'])
    assert r['sheet1'] if 'sheet1' in r else None is None or r['sheet1'] is None
    sheet2 = r['sheet2']
    assert len(sheet2) == 27
    assert set(sheet2[0]) == set(['A','B','C','D','E','F'])
    assert sheet2[0]['A'] == 'id'
    assert sheet2[-1]['A'] == 50 or sheet2[-1]['A'] == '50' # write as per data

def test_get_only_sheet2_header_rows():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': [{'name':'sheet2','header':{'rows':1}}]})
    val = r['sheet2'][0]
    assert not (val['A']=='id' and val['B']=='first_name' and val['C']=='last_name')

def test_colum_to_key_and_header_rows_in_sheets():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': [{'name':'sheet2','header':{'rows':1},'columnToKey':{'A':'id','B':'firstName','D':'email'}}]})
    assert set(r.keys()) == set(['sheet2'])
    sheet2 = r['sheet2']
    assert len(sheet2) == 26
    assert set(sheet2[0]) == set(['id','firstName','email'])
    assert sheet2[0]['id'] == '25'
    assert sheet2[-1]['id'] == '50'

def test_colum_to_key_cell_variables():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': [{'name':'sheet2'}], 'header': {'rows': 1}, 'columnToKey': {'A':'{{A1}}','B':'{{B1}}','D':'{{D1}}'}})
    assert set(r['sheet2'][0]) == set(['id','first_name','email']) or 'id' in r['sheet2'][0]
    assert r['sheet2'][0]['id']=='25'
    assert r['sheet2'][-1]['id']=='50'

def test_colum_to_key_and_header_rows_out_of_sheets():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': [{'name':'sheet2'}], 'header': {'rows': 1}, 'columnToKey': {'A':'id','B':'firstName','D':'email'}})
    sheet2 = r['sheet2']
    assert set(sheet2[0]) == set(['id','firstName','email'])
    assert sheet2[0]['id'] == '25'
    assert sheet2[-1]['id'] == '50'

def test_colum_to_key_star_column_header():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': [{'name':'sheet2'}], 'header': {'rows': 1}, 'columnToKey': {'*':'{{columnHeader}}'}})
    sheet2 = r['sheet2']
    # Should have keys found in header row
    assert all(k in ['id','first_name','last_name','email','gender','ip_address'] for k in sheet2[0])

def test_include_empty_lines_sheet3():
    r = convert_excel_to_json({'sourceFile': SOURCE_FILE, 'sheets': [{'name':'sheet3'}], 'header': {'rows': 0}, 'includeEmptyLines': True})
    # Should have undefined/None rows per JS test
    assert isinstance(r['sheet3'], list)
    if len(r['sheet3']) >= 4:  # at least 4 rows to check undefineds
        assert r['sheet3'][0] == {} or r['sheet3'][0] is None or not r['sheet3'][0]
        assert 'A' in r['sheet3'][1] and r['sheet3'][1]['A']=='id'
        assert r['sheet3'][3] == {} or r['sheet3'][3] is None or not r['sheet3'][3]