import pytest
from rajinipp.lexer import Lexer
from rajinipp.utils import read_yml

def test_public_lexer_tokenization_for_identifier():
    tokens = read_yml("rajinipp/token.yml")
    lexer = Lexer(tokens).get_lexer()
    result = list(lexer.lex("varX1 = 9"))
    # Should include an identifier
    token_names = [tok.name for tok in result]
    assert "ID" in token_names

def test_public_lexer_ignores_comments():
    tokens = read_yml("rajinipp/token.yml")
    lexer = Lexer(tokens).get_lexer()
    code = "num = 2  !! this is a comment\nprint num"
    result = list(lexer.lex(code))
    code_fragment = " ".join([tok.value for tok in result if hasattr(tok, "value")])
    assert "!!" not in code_fragment

# Exception test: if token file missing
def test_public_lexer_raise_file_exception(monkeypatch):
    def bad_read_yml(_):
        raise FileNotFoundError("no such file")
    import rajinipp.lexer
    monkeypatch.setattr(rajinipp.lexer, "read_yml", bad_read_yml)
    with pytest.raises(FileNotFoundError):
        _ = rajinipp.lexer.Lexer(None)  # Should indirectly attempt token file read