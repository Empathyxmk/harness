import pytest

def deflateimports(input_val):
    """
    Deflates structures or lists of structures containing 'import' fields,
    flattening multiple 'import' fields into a single cell (list), for testing.
    """
    from copy import deepcopy

    # Helper: merge imports in cell/list
    def merge_imports(lst):
        imports = []
        data = []
        for item in lst:
            if isinstance(item, dict) and 'import' in item:
                imp = item['import']
                if isinstance(imp, str):
                    imports.append(imp)
                elif isinstance(imp, list):
                    imports.extend(imp)
            else:
                data.append(item)
        if imports:
            data.append({'import': imports})
        return data

    # If dict with 'import'
    if isinstance(input_val, dict):
        new_input = deepcopy(input_val)
        for key, value in new_input.items():
            if key == 'import':
                if isinstance(value, str):
                    new_input[key] = [value]
                elif isinstance(value, list):
                    new_input[key] = value
            elif isinstance(value, dict) or isinstance(value, list):
                new_input[key] = deflateimports(value)
        return new_input
    # If list/cell
    elif isinstance(input_val, list):
        return merge_imports([deflateimports(item) if isinstance(item, (dict, list)) else item for item in input_val])
    # Return unchanged for others
    else:
        return input_val

def test_no_import_field():
    input_ = {'a': 1, 'b': 'test'}
    expected = {'a': 1, 'b': 'test'}
    result = deflateimports(input_)
    assert result == expected, "Should return the input unchanged."

def test_no_import_in_cell():
    input_ = ['a', 1, {'field': 'value'}]
    expected = ['a', 1, {'field': 'value'}]
    result = deflateimports(input_)
    assert result == expected, "Should return the input unchanged."

def test_single_import_field_struct():
    input_ = {'import': 'file1'}
    expected = {'import': ['file1']}
    result = deflateimports(input_)
    assert result == expected, "Should wrap single import string in a cell (list)."

def test_single_import_field_cell():
    input_ = {'import': ['file1', 'file2']}
    expected = {'import': ['file1', 'file2']}
    result = deflateimports(input_)
    assert result == expected, "Should keep cell array imports as is."

def test_struct_with_nested_import():
    input_ = {'level1': {'import': 'nested_file'}}
    expected = {'level1': {'import': ['nested_file']}}
    result = deflateimports(input_)
    assert result == expected, "Should deflate nested import."

def test_cell_with_multiple_imports():
    input_ = [
        {'import': 'A'},
        {'import': ['B', 'C']},
        'other_data'
    ]
    # Expected: all imports merged into one at the end
    expected_data_present = ['other_data']
    result = deflateimports(input_)
    # There should be two items: data and the merged import dict
    assert len(result) == 2, "Result cell array length mismatch."
    assert any(item == 'other_data' for item in result), "Missing other_data."
    import_struct = next(item for item in result if isinstance(item, dict) and 'import' in item)
    assert set(import_struct['import']) == {'A', 'B', 'C'}, "Merged imports not correct."
    assert len(import_struct['import']) == 3, "Incorrect number of collected imports."

def test_cell_with_mixed_content_and_imports():
    input_ = [
        'item1',
        {'import': 'imp1'},
        {'key': 'value'},
        {'import': ['imp2', 'imp3']}
    ]
    result = deflateimports(input_)
    # Should be item1, struct({'key': 'value'}), and merged import struct
    assert len(result) == 3, "Expected 3 items after deflation (2 data + 1 combined import)."
    assert any(item == 'item1' for item in result), "item1 should be present."
    assert any(isinstance(item, dict) and item.get('key') == 'value' for item in result), "struct('key','value') should be present."
    import_struct = next(item for item in result if isinstance(item, dict) and 'import' in item)
    assert set(import_struct['import']) == {'imp1', 'imp2', 'imp3'}
    assert len(import_struct['import']) == 3

def test_empty_input():
    result = deflateimports([])
    assert result == [], "Empty input should result in empty output."

def test_input_is_matrix():
    input_ = [[1, 2], [3, 4]]
    result = deflateimports(input_)
    assert result == input_, "Matrix input should be returned as is."

def test_input_is_string():
    input_ = 'test_string'
    result = deflateimports(input_)
    assert result == input_, "String input should be returned as is."

def test_input_is_number():
    input_ = 123
    result = deflateimports(input_)
    assert result == input_, "Numeric input should be returned as is."