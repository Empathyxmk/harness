import unittest
from pj import parser

class TestParserPublic(unittest.TestCase):
    def test_parse_empty_list(self):
        tokens = ['[', ']']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, [])
        self.assertEqual(rest, [])

    def test_parse_int_array(self):
        tokens = ['[', 99, ',', 88, ']']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, [99, 88])
        self.assertEqual(rest, [])

    def test_parse_float_and_null(self):
        tokens = ['[', 1.5, ',', None, ']']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, [1.5, None])
        self.assertEqual(rest, [])

    def test_parse_object_with_array(self):
        tokens = ['{', 'items', ':', '[', 2, ',', 3, ']', '}']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, {'items': [2, 3]})
        self.assertEqual(rest, [])

    def test_parse_object_with_nested_obj(self):
        tokens = ['{', 'a', ':', '{', 'b', ':', 1, '}', '}']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, {'a': {'b': 1}})
        self.assertEqual(rest, [])

    def test_parse_bools(self):
        tokens = ['[', True, ',', False, ']']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, [True, False])
        self.assertEqual(rest, [])

    def test_parse_string_and_whitespace(self):
        tokens = ['[', 'hi', ',', 'world', ']']
        value, rest = parser.parse(tokens)
        self.assertEqual(value, ['hi', 'world'])
        self.assertEqual(rest, [])


if __name__ == "__main__":
    unittest.main()