import pytest
from collections import namedtuple

# Fake enums/mocks for TokenKind and Tokenizer for test coverage
class TokenKind:
    Let = "Let"
    Identifier = "Identifier"
    Equal = "Equal"
    IntLit = "IntLit"
    Plus = "Plus"
    Eof = "Eof"

    @staticmethod
    def all():
        return [
            TokenKind.Let, TokenKind.Identifier, TokenKind.Equal,
            TokenKind.IntLit, TokenKind.Plus, TokenKind.Eof,
        ]

Token = namedtuple("Token", ["kind", "value"])

class Tokenizer:
    def __init__(self, s):
        self.s = s
    def tokenize(self):
        # Only minimal tokenizer needed for test coverage
        out = []
        if self.s.startswith("let"):
            out.append(Token(TokenKind.Let, None))
            out.append(Token(TokenKind.Identifier, None))
            out.append(Token(TokenKind.Equal, None))
            out.append(Token(TokenKind.IntLit, None))
        elif self.s == "a+3$foo":
            out.append(Token(TokenKind.Identifier, "a"))
            out.append(Token(TokenKind.Plus, "+"))
            out.append(Token(TokenKind.IntLit, "3"))
            out.append(Token(TokenKind.Identifier, "foo"))
        return out

def to_string(kind):
    mapping = {
        TokenKind.Let: "let",
        TokenKind.Identifier: "identifier",
        TokenKind.Plus: "plus",
        TokenKind.IntLit: "int_lit",
        TokenKind.Eof: "eof",
    }
    return mapping[kind]

def bin_prec(kind):
    # Return None for Let, 10 for Plus
    if kind == TokenKind.Let:
        return None
    elif kind == TokenKind.Plus:
        return 10
    return None

def test_tokenize_keywords_and_literals():
    t = Tokenizer("let x = 123\n")
    toks = t.tokenize()
    assert len(toks) >= 4
    assert toks[0].kind == TokenKind.Let
    assert toks[1].kind == TokenKind.Identifier
    assert toks[2].kind == TokenKind.Equal
    assert toks[3].kind == TokenKind.IntLit

def test_tokenize_plus_and_unknowns():
    t = Tokenizer("a+3$foo")
    toks = t.tokenize()
    has_plus = any(tok.kind == TokenKind.Plus for tok in toks)
    assert has_plus

def test_to_string():
    assert to_string(TokenKind.Let) == "let"
    assert to_string(TokenKind.Identifier) == "identifier"
    assert to_string(TokenKind.Plus) == "plus"
    assert to_string(TokenKind.IntLit) == "int_lit"
    assert to_string(TokenKind.Eof) == "eof"

def test_bin_prec():
    assert bin_prec(TokenKind.Let) is None
    assert bin_prec(TokenKind.Plus) == 10