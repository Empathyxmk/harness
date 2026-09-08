import pytest
from sql_metadata.token import SQLToken
import sqlparse
from sqlparse.tokens import Keyword, Name, Punctuation, Wildcard, Number, Comment

def test_empty_sqltoken_defaults():
    token = SQLToken()
    assert token.value == ""
    assert token.is_keyword is False
    assert token.is_name is False
    assert token.is_punctuation is False
    assert token.is_dot is False
    assert token.is_wildcard is False
    assert token.is_integer is False
    assert token.is_float is False
    assert token.is_comment is False
    assert token.is_as_keyword is False
    assert token.is_left_parenthesis is False
    assert token.is_right_parenthesis is False
    assert token.normalized == ""
    assert str(token) == ""
    assert token.previous_token is None
    assert token.next_token is None

def make_token(value, ttype):
    return sqlparse.sql.Token(ttype, value)

def test_sqltoken_types_parsing():
    name_tok = make_token("foo", Name)
    kw_tok = make_token("SELECT", Keyword)
    dot_tok = make_token(".", Punctuation)
    int_tok = make_token("123", Number.Integer)
    float_tok = make_token("1.23", Number.Float)
    comm_tok = make_token("-- comment", Comment)
    wc_tok = make_token("*", Wildcard)
    punct_tok = make_token(",", Punctuation)

    sql_token = SQLToken(name_tok)
    assert sql_token.value == "foo"
    assert sql_token.is_name
    assert not sql_token.is_keyword

    sql_token_kw = SQLToken(kw_tok)
    assert sql_token_kw.is_keyword
    assert not sql_token_kw.is_name

    sql_token_dot = SQLToken(dot_tok)
    assert sql_token_dot.is_dot
    assert sql_token_dot.is_punctuation

    sql_token_int = SQLToken(int_tok)
    assert sql_token_int.is_integer

    sql_token_float = SQLToken(float_tok)
    assert sql_token_float.is_float

    sql_token_comment = SQLToken(comm_tok)
    assert sql_token_comment.is_comment

    sql_token_wc = SQLToken(wc_tok)
    assert sql_token_wc.is_wildcard

    sql_token_punct = SQLToken(punct_tok)
    assert sql_token_punct.is_punctuation

    # test normalization
    assert sql_token_kw.normalized == "SELECT"
    assert sql_token.normalized == "FOO"

def test_sqltoken_stringified_token_spacing():
    tokens = [
        SQLToken(sqlparse.sql.Token(Keyword, "SELECT")),
        SQLToken(sqlparse.sql.Token(Name, "foo")),
        SQLToken(sqlparse.sql.Token(Punctuation, ",")),
        SQLToken(sqlparse.sql.Token(Name, "bar")),
        SQLToken(sqlparse.sql.Token(Punctuation, "(")),
    ]
    # link tokens, simulating a token list in real usage
    for i in range(1, len(tokens)):
        tokens[i].previous_token = tokens[i-1]
    out = [t.stringified_token for t in tokens]
    # first token: SELECT (should be prefixed by a space per implementation)
    assert out[0] == " SELECT"
    # name token - should be prefixed by a space
    assert out[1].startswith(" ") and "foo" in out[1]
    # comma should have NO space (default behavior for punctuation)
    assert out[2] == ","
    # bar should be prefixed with a space
    assert out[3].startswith(" ") and "bar" in out[3]
    # ( should have NO space before
    assert out[4] == "("

def test_last_keyword_normalized_and_str_repr():
    name_tok = make_token("foo", Name)
    sql_token = SQLToken(name_tok, last_keyword="select")
    # last_keyword_normalized uppercases, strips spaces
    assert sql_token.last_keyword_normalized == "SELECT"
    assert isinstance(str(sql_token), str)
    assert "foo" in str(sql_token)

def test_repr_does_work():
    kw_tok = make_token("SELECT", Keyword)
    sql_token = SQLToken(kw_tok)
    # __repr__ isn't covered by default, but force coverage
    rep = sql_token.__repr__()
    assert "SQLToken" in rep
    assert "SELECT" in rep