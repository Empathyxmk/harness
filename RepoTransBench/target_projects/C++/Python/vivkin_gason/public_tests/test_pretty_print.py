import json
import os
import pytest

TESTDATA = [
    {
        "input": "{\"hello\": 321, \"answer\": [77, 88, 99], \"valid\": false, \"msg\": \"Hi\", \"pi\": 3.142}",
        "expected": "{\n    \"hello\": 321.000000,\n    \"answer\": [\n        77.000000,\n        88.000000,\n        99.000000\n    ],\n    \"valid\": false,\n    \"msg\": \"Hi\",\n    \"pi\": 3.142000\n}\n"
    },
    {
        "input": "[{\"z\": 22}, {\"y\": 33}]",
        "expected": "[\n    {\n        \"z\": 22.000000\n    },\n    {\n        \"y\": 33.000000\n    }\n]\n"
    },
    {
        "input": "{\"emptyArr\": [], \"emptyObj\": {}}",
        "expected": "{\n    \"emptyArr\": [],\n    \"emptyObj\": {}\n}\n"
    },
    {
        "input": "1234567",
        "expected": "1234567.000000\n"
    },
    {
        "input": "\"newStringTest\"",
        "expected": "\"newStringTest\"\n"
    },
    {
        "input": "{\"values\": [10, 20, 30], \"msg\": \"Test done!\", \"tmpBool\": true}",
        "expected": "{\n    \"values\": [\n        10.000000,\n        20.000000,\n        30.000000\n    ],\n    \"msg\": \"Test done!\",\n    \"tmpBool\": true\n}\n"
    },
    {
        "input": "[false, 0, null, \"ok\"]",
        "expected": "[\n    false,\n    0.000000,\n    null,\n    \"ok\"\n]\n"
    },
    {
        "input": "{\"k\": [1, [2, [3, [4]]]]}",
        "expected": "{\n    \"k\": [\n        1.000000,\n        [\n            2.000000,\n            [\n                3.000000,\n                [\n                    4.000000\n                ]\n            ]\n        ]\n    ]\n}\n"
    },
    {
        "input": "[[3.14], [2.718], [1.414]]",
        "expected": "[\n    [\n        3.140000\n    ],\n    [\n        2.718000\n    ],\n    [\n        1.414000\n    ]\n]\n"
    },
    {
        "input": "{\"nested\": {\"x\": [5, 6], \"y\": {\"key\": \"val\"}}}",
        "expected": "{\n    \"nested\": {\n        \"x\": [\n            5.000000,\n            6.000000\n        ],\n        \"y\": {\n            \"key\": \"val\"\n        }\n    }\n}\n"
    }
]


def pretty_print_json(obj, indent=4):
    """
    Tries to mimic the pretty-printed output as appears in the expected C++ output.
    Uses .000000 for numbers, handles strings and booleans as shown.
    """
    def format_item(item, level):
        prefix = ' ' * (indent * level)
        if isinstance(item, dict):
            if len(item) == 0:
                return '{}'
            items = []
            for i, (k, v) in enumerate(item.items()):
                items.append(f'{prefix}{" " * indent}"{k}": {format_item(v, level + 1)}')
            return ('{\n' +
                    ',\n'.join(items) +
                    f'\n{prefix}}}')
        elif isinstance(item, list):
            if len(item) == 0:
                return '[]'
            items = []
            for v in item:
                items.append(f'{prefix}{" " * indent}{format_item(v, level + 1)}')
            return ('[\n' +
                    ',\n'.join(items) +
                    f'\n{prefix}]')
        elif isinstance(item, bool):
            return 'true' if item else 'false'
        elif item is None:
            return 'null'
        elif isinstance(item, (int, float)):
            # Pad all numbers to 6 decimal places
            return f'{item:.6f}'
        elif isinstance(item, str):
            # Make sure to handle proper JSON escaping for strings
            return json.dumps(item)
        else:
            raise Exception("Unknown type in pretty print: {}".format(type(item)))
    try:
        output = format_item(obj, 0)
        # Add a trailing newline, as all C++ pretty-print cases end with '\n'
        return output + '\n'
    except Exception as ex:
        raise

@pytest.mark.parametrize("case", TESTDATA)
def test_pretty_print(case):
    # Try to parse the input using Python's json module
    try:
        obj = json.loads(case["input"])
    except Exception as e:
        pytest.fail(f"Failed to parse test input as JSON: {case['input']}\nError: {e}")
    expected = case["expected"]
    actual = pretty_print_json(obj)
    # Output comparisons can be sensitive to whitespace, so test strictly
    assert actual == expected, f"Pretty print failed.\nInput:\n{case['input']}\nExpected:\n{expected!r}\nGot:\n{actual!r}\n"