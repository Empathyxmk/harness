import pytest

def get_string_or_buffer_from_value_mock_string(input_str):
    # Simulate the "string" branch logic from C++
    o_data = input_str
    return True, o_data

def get_string_or_buffer_from_value_mock_buffer(data):
    # Simulate the "buffer" branch logic from C++
    o_data = data
    return True, o_data

def get_string_or_buffer_from_value_mock_other():
    # Simulate the "other" branch logic from C++
    o_data = ""
    return False, o_data

def test_public_string_input():
    result, output = get_string_or_buffer_from_value_mock_string("public_input")
    assert result is True
    assert output == "public_input"

def test_public_buffer_input():
    input_data = "test_data_123"
    result, output = get_string_or_buffer_from_value_mock_buffer(input_data)
    assert result is True
    assert output == "test_data_123"

def test_public_other_input():
    result, output = get_string_or_buffer_from_value_mock_other()
    assert result is False
    assert output == ""