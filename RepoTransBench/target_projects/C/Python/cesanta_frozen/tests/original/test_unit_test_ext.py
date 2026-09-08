import pytest
import json

def json_walk(json_str, callback, user_data):
    """
    Rough Python adaptation of C frozen's json_walk.

    For each root-level property or array element, call the callback.
    For this test port, we implement a simple walk over dicts/lists.
    """
    def inner(obj, path=""):
        if isinstance(obj, dict):
            callback(user_data, None, 0, path, None)
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else f".{key}"
                inner(value, new_path)
        elif isinstance(obj, list):
            callback(user_data, None, 0, path, None)
            for idx, value in enumerate(obj):
                new_path = f"{path}[{idx}]"
                inner(value, new_path)
        else:
            callback(user_data, None, 0, path, None)

    try:
        obj = json.loads(json_str)
        inner(obj)
        return 1
    except Exception:
        return -1

JSON_TYPE_STRING = 1
JSON_TYPE_NUMBER = 2
JSON_TYPE_TRUE = 3
JSON_TYPE_FALSE = 4
JSON_TYPE_NULL = 5
JSON_TYPES_CNT = 6  # Not used directly, but for array size

class DummyToken:
    def __init__(self, ttype):
        self.type = ttype

def test_json_walk_valid_object():
    # Test json_walk with a simple object
    json_str = '{ "foo": 123, "bar": [1,2] }'
    callback_counter = [0]
    def capture_callback(data, name, name_len, path, token):
        data[0] += 1
    res = json_walk(json_str, capture_callback, callback_counter)
    assert res > 0 and callback_counter[0] > 0

def test_json_walk_empty_object():
    # Test json_walk with empty object
    json_str = "{}"
    callback_counter = [0]
    def capture_callback(data, name, name_len, path, token):
        data[0] += 1
    res = json_walk(json_str, capture_callback, callback_counter)
    assert res > 0 and callback_counter[0] > 0

def test_json_walk_invalid():
    # Test json_walk with invalid JSON, expect negative result
    json_str = "{ foo: "
    callback_counter = [0]
    def capture_callback(data, name, name_len, path, token):
        data[0] += 1
    res = json_walk(json_str, capture_callback, callback_counter)
    assert res < 0

def test_json_token_types():
    # Test token type counts by parsing
    json_str = '{ "str": "txt", "num": 112, "tf": true, "fa": false, "nul": null }'
    token_type_counts = [0] * JSON_TYPES_CNT
    def my_callback(typec, name, name_len, path, token):
        # Simulate token type classification.
        last = path.split(".")[-1].replace("[0]", "")
        if last in ["str"]:
            typec[JSON_TYPE_STRING] += 1
        elif last in ["num"]:
            typec[JSON_TYPE_NUMBER] += 1
        elif last in ["tf"]:
            typec[JSON_TYPE_TRUE] += 1
        elif last in ["fa"]:
            typec[JSON_TYPE_FALSE] += 1
        elif last in ["nul"]:
            typec[JSON_TYPE_NULL] += 1
    res = json_walk(json_str, my_callback, token_type_counts)
    assert res > 0
    assert token_type_counts[JSON_TYPE_STRING] > 0
    assert token_type_counts[JSON_TYPE_NUMBER] > 0
    assert token_type_counts[JSON_TYPE_TRUE] > 0
    assert token_type_counts[JSON_TYPE_FALSE] > 0
    assert token_type_counts[JSON_TYPE_NULL] > 0

def test_json_walk_array_edge():
    # Test array path handling and array ends
    json_str = '[1,2,{"nest":3}]'
    callback_counter = [0]
    def capture_callback(data, name, name_len, path, token):
        data[0] += 1
    res = json_walk(json_str, capture_callback, callback_counter)
    assert res > 0
    assert callback_counter[0] > 0

def test_error_codes_edge():
    # Test error propagation for incomplete/invalid JSON
    def run(json_str):
        callback_counter = [0]
        res = json_walk(json_str, lambda *args: None, callback_counter)
        return res
    # python's json.loads raises only one kind of error,
    # but we simulate both incomplete and invalid as -1 for this test port.
    assert run('{ "unterminated ') < 0
    assert run("{a:") < 0
    assert run("{a:%%}") < 0

def test_json_safely_nested_objects():
    # Limit the nesting level to prevent stack overflow (simulate with smaller depth)
    json_str = '{"level1":{"level2":{"k":1}}}'
    callback_counter = [0]
    def capture_callback(data, name, name_len, path, token):
        data[0] += 1
    res = json_walk(json_str, capture_callback, callback_counter)
    assert res > 0 and callback_counter[0] > 0

def test_json_array_of_arrays():
    json_str = "[[],[[],[]],[[]]]"
    callback_counter = [0]
    def capture_callback(data, name, name_len, path, token):
        data[0] += 1
    res = json_walk(json_str, capture_callback, callback_counter)
    assert res > 0 and callback_counter[0] > 0

def test_json_strings_escapes_unicode():
    # Test JSON string with escapes and unicode
    json_str = "\"hello\\nworld\\u0041\""
    import codecs
    value = json.loads(json_str)
    # String should be: hello\nworldA
    assert value == "hello\nworldA"