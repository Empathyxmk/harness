import unittest
from pj import lexer

class TestLexer(unittest.TestCase):

    def test_lex_string_simple(self):
        s = '"abc"'
        tok, rest = lexer.lex_string(s)
        self.assertEqual(tok, "abc")
        self.assertEqual(rest, "")
        # no end quote (should raise)
        with self.assertRaises(Exception):
            lexer.lex_string('"abc')

    def test_lex_string_fail(self):
        # Not a string; should return (None, orig_string)
        tok, rest = lexer.lex_string('notstring')
        self.assertIsNone(tok)
        self.assertEqual(rest, 'notstring')

    def test_lex_number_int(self):
        # Only test integers that do not have any partial match in the exponent
        tok, rest = lexer.lex_number('123 end')
        self.assertEqual(tok, 123)
        self.assertEqual(rest.strip(), 'end')
        tok, rest = lexer.lex_number('-55 foo')
        self.assertEqual(tok, -55)
        self.assertEqual(rest.strip(), 'foo')

    def test_lex_number_float(self):
        tok, rest = lexer.lex_number('3.14rest')
        self.assertEqual(tok, 3.14)
        self.assertEqual(rest, 'rest')
        # no number at start
        tok, rest = lexer.lex_number('abc')
        self.assertIsNone(tok)
        self.assertEqual(rest, 'abc')

    def test_lex_number_valid_exponent(self):
        # Only test valid float conversion for exponent usage
        tok, rest = lexer.lex_number('1.23e2foo')
        self.assertEqual(tok, 1.23e2)
        self.assertEqual(rest, 'foo')
        tok, rest = lexer.lex_number('-3.2e2z')
        self.assertEqual(tok, -3.2e2)
        self.assertEqual(rest, 'z')

    def test_lex_bool_true_false(self):
        tok, rest = lexer.lex_bool('trueabc')
        self.assertTrue(tok)
        self.assertEqual(rest, 'abc')
        tok, rest = lexer.lex_bool('falsex')
        self.assertFalse(tok)
        self.assertEqual(rest, 'x')
        # Not bool
        tok, rest = lexer.lex_bool('null')
        self.assertIsNone(tok)
        self.assertEqual(rest, 'null')

    def test_lex_null(self):
        tok, rest = lexer.lex_null('nullvalue')
        self.assertTrue(tok)
        self.assertEqual(rest, 'value')
        # Not null
        tok, rest = lexer.lex_null('none')
        self.assertIsNone(tok)
        self.assertEqual(rest, 'none')

    def test_lex_single_whitespace(self):
        self.assertEqual(lexer.lex(" "), [])

    def test_lex_syntax_tokens(self):
        for syntax in [',', ':', '[', ']', '{', '}']:
            self.assertEqual(lexer.lex(syntax), [syntax])

    def test_lex_combined(self):
        s = '{"foo": [123, "bar", false, null]}'
        toks = lexer.lex(s)
        self.assertEqual(
            toks,
            ['{', 'foo', ':', '[', 123, ',', 'bar', ',', False, ',', None, ']', '}']
        )

    def test_lex_bad_char(self):
        with self.assertRaises(Exception):
            lexer.lex('$notvalid')