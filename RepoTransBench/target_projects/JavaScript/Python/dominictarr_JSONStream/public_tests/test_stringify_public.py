from src.jsonstream import jsonstream

def test_stringify_array_of_numbers_with_custom_sep():
    stringify_stream = jsonstream.stringify('[', ']', ';')
    input_data = [100, 200, 300]
    result = ''
    for chunk in stringify_stream.write_items(input_data):
        result += chunk
    assert result == '[100;200;300]'

def test_stringify_array_of_objects_with_alternative_data():
    stringify_stream = jsonstream.stringify('[', ']', ',')
    input_data = [
        {'id': 5, 'pet': "Dog"},
        {'id': 3, 'pet': "Cat"},
        {'id': 15, 'pet': "Rabbit"}
    ]
    result = ''
    for chunk in stringify_stream.write_items(input_data):
        result += chunk
    import json
    assert json.loads(result) == input_data

def test_stringify_single_string_value_with_custom_delim():
    stringify_stream = jsonstream.stringify('||', '||', '-')
    result = ''
    for chunk in stringify_stream.write_items(['hello']):
        result += chunk
    assert result == '||"hello"||'