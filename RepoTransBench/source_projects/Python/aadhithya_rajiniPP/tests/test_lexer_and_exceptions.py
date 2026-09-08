import pytest
from munch import Munch
from rajinipp.lexer import Lexer
from rajinipp import exceptions

def test_lexer_add_and_get_tokens():
    # Basic tokens: just a couple for smoke test
    tokens = Munch(NUM="\\d+", PLUS="\\+")
    lexer = Lexer(tokens)
    lex_obj = lexer.get_lexer()
    # Check that the returned object has 'lex' method (from rply lexer)
    assert hasattr(lex_obj, "lex")
    result = list(lex_obj.lex("3 + 5"))
    assert {t.name for t in result} == {"NUM", "PLUS"}

def test_lexer_ignore_comments_and_whitespace():
    tokens = Munch(ID="[a-zA-Z_]+", EQ="=")
    lexer = Lexer(tokens)
    lex_obj = lexer.get_lexer()
    # "!!" starts a comment (should be ignored)
    code = "foo = bar   !! this is a comment\nbaz=qux"
    result = [t for t in lex_obj.lex(code)]
    assert [t.name for t in result] == ["ID", "EQ", "ID", "ID", "EQ", "ID"]

def test_break_exception():
    with pytest.raises(exceptions.BreakException):
        raise exceptions.BreakException("Break now")

def test_return_exception_value():
    msg = "Return!"
    ret_val = 42
    with pytest.raises(exceptions.ReturnException) as excinfo:
        raise exceptions.ReturnException(msg, ret_val)
    assert excinfo.value.return_value == ret_val
    assert msg in str(excinfo.value)