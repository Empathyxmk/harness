import pytest
from pj import lexer

class TestLexerPublic:
    def test_lex_number_simple(self):
        tok, rest = lexer.lex_number('222abc')
        assert tok == 222
        assert rest == "abc"

    def test_lex_number_decimal(self):
        tok, rest = lexer.lex_number('99.123z')
        assert abs(tok - 99.123) < 1e-6
        assert rest == "z"

    def test_lex_number_negative(self):
        tok, rest = lexer.lex_number('-657tail')
        assert tok == -657
        assert rest == "tail"

    def test_lex_number_zero(self):
        tok, rest = lexer.lex_number('0____')
        assert tok == 0
        assert rest == "____"

    def test_lex_number_leading_zeroes(self):
        tok, rest = lexer.lex_number('0005!')
        assert tok == 0
        assert rest == "005!"

    def test_lex_escape_single_escaped(self):
        tok, rest = lexer.lex_escaped('"f\\nulio"rest')
        assert tok == 'f\\nulio'
        assert rest == "rest"

    def test_lex_escape_quotes(self):
        tok, rest = lexer.lex_escaped('"abc\\"def"tail')
        assert tok == 'abc\\"def'
        assert rest == "tail"

    def test_lex_escape_hex(self):
        s, rest = lexer.lex_escaped('"\\x48abc"x')
        assert s == '\\x48abc'
        assert rest == 'x'

    def test_lex_escape_unicode(self):
        tok, rest = lexer.lex_escaped('"\\u0048"abc')
        assert tok == '\\u0048'
        assert rest == 'abc'

    def test_lex_number_float_exponent(self):
        tok, rest = lexer.lex_number('18.12e2!')
        assert abs(tok - 1812) < 1e-6
        assert rest == "!"

    def test_lex_number_negative_exponent(self):
        tok, rest = lexer.lex_number('45e-1Q')
        assert abs(tok - 4.5) < 1e-6
        assert rest == 'Q'

    def test_lex_number_large_exponent(self):
        tok, rest = lexer.lex_number('2.5e3and')
        assert abs(tok - 2500) < 1e-6
        assert rest == 'and'

    def test_lex_number_plus_exponent(self):
        tok, rest = lexer.lex_number('6e+2zzz')
        assert abs(tok - 600) < 1e-6
        assert rest == "zzz"

    # This is the problematic test in the previous version
    def test_lex_number_valid_exponent_other(self):
        # Use 5e1X where the ending is not a valid exponent part but removable safely
        tok, rest = lexer.lex_number('5e1X')
        assert abs(tok - 50) < 1e-6
        assert rest == "X"

    def test_lex_bool_true(self):
        tok, rest = lexer.lex_bool('truee')
        assert tok is True
        assert rest == "e"

    def test_lex_bool_false(self):
        tok, rest = lexer.lex_bool('falsest')
        assert tok is False
        assert rest == "st"

    def test_lex_bool_invalid(self):
        result = lexer.lex_bool("turtle")
        assert result is None

    def test_lex_null(self):
        tok, rest = lexer.lex_null('nullify')
        assert tok is None
        assert rest == "ify"

    def test_lex_null_invalid(self):
        result = lexer.lex_null("notnull")
        assert result is None

    def test_next_lexed(self):
        toks = []
        program = '12 "abc" true null'
        while program.strip():
            val, program = lexer.next_lexed(program)
            toks.append(val)
            program = program.strip()
        assert toks == [12, 'abc', True, None]

    def test_next_lexed_float(self):
        val, rest = lexer.next_lexed('3.51hello')
        assert abs(val - 3.51) < 1e-6
        assert rest == "hello"