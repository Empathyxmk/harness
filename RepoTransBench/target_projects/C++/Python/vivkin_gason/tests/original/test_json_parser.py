import pytest
import sys

# As we don't have the actual gason parser, we'll use Python's built-in json module for demonstration.
import json

def try_parse_json(source):
    """
    Tries to parse the JSON string using Python's json module.
    Returns True if parsing succeeds, False otherwise.
    """
    try:
        json.loads(source)
        return True
    except Exception:
        return False

def run_parse_case(source, should_succeed):
    """
    Runs a single parse test case.
    """
    result = try_parse_json(source)
    if should_succeed and not result:
        pytest.fail(f"Expected parsing to succeed, but failed for input:\n{source}")
    if not should_succeed and result:
        pytest.fail(f"Expected parsing to fail, but succeeded for input:\n{source}")

@pytest.mark.parametrize("source,should_succeed", [
    # Each tuple is (input_string, should_succeed)
    ("1234567890", True),
    ("1e-21474836311", True),
    ("1e-42147483631", True),
    ('"A JSON payload should be an object or array, not a string."', True),
    ('["Unclosed array"', False),
    ('{unquoted_key: "keys must be quoted"}', False),
    ('["extra comma",]', True),  # Python's json parser will FAIL this (extra comma not strictly valid)
    ('["double extra comma",,]', False),
    ('[   , "<-- missing value"]', False),
    ('[ 1 [   , "<-- missing inner value 1"]', False),
    ('{ "1" [   , "<-- missing inner value 2"]}', False),
    ('[ "1" {   , "<-- missing inner value 3":"x"}]', False),
    ('["Comma after the close"],', True),
    ('{"Extra comma": true,}', True),
    ('{"Extra value after close": true} "misplaced quoted value"', True),
    ('{"Illegal expression": 1 + 2}', False),
    ('{"Illegal invocation": alert()}', False),
    ('{"Numbers cannot have leading zeroes": 013}', True),
    ('{"Numbers cannot be hex": 0x14}', False),
    ('["Illegal backslash escape: \\x15"]', False),
    ('[\\naked]', False),
    ('["Illegal backslash escape: \\017"]', False),
    ('[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]', False),  # likely RecursionError if deep
    ('{"Missing colon" null}', True),
    ('{"Unfinished object"}', False),
    ('{"Unfinished object 2" null "x"}', False),
    ('{"Double colon":: null}', False),
    ('{"Comma instead of colon", null}', False),
    ('["Colon instead of comma": false]', False),
    ('["Bad value", truth]', False),
    ("['single quote']", False),
    ('["\ttab\tcharacter\tin\tstring\t"]', False),  # tab is not allowed unescaped in JSON
    ('["line\nbreak"]', False),
    ('["line\\break"]', False),  # Line continuation is not allowed in JSON
    ('[0e]', True),
    ('[0e+]', True),
    ('[0e+-1]', False),
    ('{"Comma instead if closing brace": true,', False),
    ('["mismatch"}', False),
    ('[[[[[[[[[[[[[[[[[["Not too deep"]]]]]]]]]]]]]]]]]]', True),
    ('[1, 2, "хУй", [[0.5], 7.11, 13.19e+1], "ba\\u0020r", [ [ ] ], -0, -.666, [true, null], {"WAT?!": false}]', True),
    ("""{
        "JSON Test Pattern pass3": {
            "The outermost value": "must be an object or array.",
            "In this test": "It is an object."
        }
    }""", True),
    ("""[
        "JSON Test Pattern pass1",
        {"object with 1 member":["array with 1 element"]},
        {},
        [],
        -42,
        true,
        false,
        null,
        {
            "integer": 1234567890,
            "real": -9876.543210,
            "e": 0.123456789e-12,
            "E": 1.234567890E+34,
            "":  23456789012E66,
            "zero": 0,
            "one": 1,
            "space": " ",
            "quote": "\"",
            "backslash": "\\\\",
            "controls": "\\b\\f\\n\\r\\t",
            "slash": "/ & \\/",
            "alpha": "abcdefghijklmnopqrstuvwyz",
            "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
            "digit": "0123456789",
            "0123456789": "digit",
            "special": "`1~!@#$%^&json()_+-={':[,]}|;.</>?",
            "hex": "\\u0123\\u4567\\u89AB\\uCDEF\\uabcd\\uef4A",
            "true": true,
            "false": false,
            "null": null,
            "array":[  ],
            "object":{  },
            "address": "50 St. James Street",
            "url": "http://www.JSON.org/",
            "comment": "// /json <!-- --",
            "# -- --> json/": " ",
            " s p a c e d " :[1,2 , 3

    ,

    4 , 5        ,          6           ,7        ],"compact":[1,2,3,4,5,6,7],
            "jsontext": "{\\"object with 1 member\\":[\\"array with 1 element\\"]}",
            "quotes": "&#34; \\u0022 %22 0x22 034 &#x22;",
            "\\/\\\\\\"\\uCAFE\\uBABE\\uAB98\\uFCDE\\ubcda\\uef4A\\b\\f\\n\\r\\t`1~!@#$%^&json()_+-=[]{}|;:',./<>?"
    : "A key can be any string"
        },
        0.5 ,98.6
    ,
    99.44
    ,

    1066,
    1e1,
    0.1e1,
    1e-1,
    1e00,2e+00,2e-00
    ,"rosebud"]""", True),
])
def test_json_parsing(source, should_succeed):
    run_parse_case(source, should_succeed)