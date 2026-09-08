import unittest
from pj import parser

class TestParser(unittest.TestCase):

    def test_parse_array_empty(self):
        val, tokens = parser.parse_array([']'])
        self.assertEqual(val, [])
        self.assertEqual(tokens, [])

    def test_parse_array_multiple(self):
        toks = [1, ',', 2, ']', 'leftover']
        arr, rest = parser.parse_array(toks)
        self.assertEqual(arr, [1, 2])
        self.assertEqual(rest, ['leftover'])

    def test_parse_array_error(self):
        # missing comma after first value
        with self.assertRaises(Exception):
            parser.parse_array([1, 2, ']'])

    def test_parse_object_empty(self):
        val, tokens = parser.parse_object(['}'])
        self.assertEqual(val, {})
        self.assertEqual(tokens, [])

    def test_parse_object_basic(self):
        toks = ['key', ':', 42, '}']
        obj, rest = parser.parse_object(toks)
        self.assertEqual(obj, {'key': 42})
        self.assertEqual(rest, [])

    def test_parse_object_multiple(self):
        toks = ['a', ':', 1, ',', 'b', ':', 2, '}', 'end']
        obj, rest = parser.parse_object(toks)
        self.assertEqual(obj, {'a': 1, 'b': 2})
        self.assertEqual(rest, ['end'])

    def test_parse_object_key_nonstring(self):
        with self.assertRaises(Exception):
            parser.parse_object([1, ':', 2, '}'])
    
    def test_parse_object_colon_missing(self):
        with self.assertRaises(Exception):
            parser.parse_object(['key', 42, '}'])

    def test_parse_object_comma_missing(self):
        # After first pair, expect , or }
        with self.assertRaises(Exception):
            parser.parse_object(['key', ':', 1, 42, '}'])

    def test_parse_array_missing_end(self):
        # missing closing ]
        with self.assertRaises(Exception):
            parser.parse_array([1, ','])

    def test_parse_object_missing_end(self):
        with self.assertRaises(Exception):
            parser.parse_object(['key', ':', 1])

    def test_parse_root_non_object(self):
        with self.assertRaises(Exception):
            parser.parse(['[', 1, ']'], is_root=True)

    def test_parse_array_delegation(self):
        arr, rest = parser.parse(['[', 1, ',', 2, ']'])
        self.assertEqual(arr, [1, 2])
        self.assertEqual(rest, [])

    def test_parse_object_delegation(self):
        obj, rest = parser.parse(['{', 'a', ':', 3, '}'])
        self.assertEqual(obj, {'a': 3})
        self.assertEqual(rest, [])

    def test_parse_literal(self):
        val, rest = parser.parse([42, ',', 100])
        self.assertEqual(val, 42)
        self.assertEqual(rest, [',', 100])