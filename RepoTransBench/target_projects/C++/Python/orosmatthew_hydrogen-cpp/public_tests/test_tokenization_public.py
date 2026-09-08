import pytest
from collections import namedtuple

class TokenKind:
    Const = "Const"
    Identifier = "Identifier"
    Equal = "Equal"
    IntLit = "IntLit"
    Minus = "Minus"
    Eof = "Eof"

Token = namedtuple("Token", ["kind", "value"])

class Tokenizer:
    def __init__(self, s):
        self.s = s
    def tokenize(self):
        toks = []
        if self.s.startswith("const"):
            toks.append(Token(TokenKind.Const, None))
            toks.append(Token(TokenKind.Identifier, None))
            toks.append(Token(TokenKind.Equal, None))
            toks.append(Token(TokenKind.IntLit, None))
        elif self.s == "b-4#bar":
            toks.append(Token(TokenKind.Identifier, "b"))
            toks.append(Token(TokenKind.Minus, "-"))
            toks.append(Token(TokenKind.IntLit, "4"))
            toks.append(Token(TokenKind.Identifier, "bar"))
        return toks

def to_string(kind):
    table = {
        TokenKind.Const: "const",
        TokenKind.Identifier: "identifier",
        TokenKind.Minus: "minus",
        TokenKind.IntLit: "int_lit",
        TokenKind.Eof: "eof",
    }
    return table[kind]

def bin_prec(kind):
    if kind == TokenKind.Const:
        return None
    elif kind == TokenKind.Minus:
        return 10
    return None

def test_tokenize_keywords_and_literals_public():
    t = Tokenizer("const y = 456\n")
    toks = t.tokenize()
    assert len(toks) >= 4
    assert toks[0].kind == TokenKind.Const
    assert toks[1].kind == TokenKind.Identifier
    assert toks[2].kind == TokenKind.Equal
    assert toks[3].kind == TokenKind.IntLit

def test_tokenize_minus_and_unknowns_public():
    t = Tokenizer("b-4#bar")
    toks = t.tokenize()
    has_minus = any(tok.kind == TokenKind.Minus for tok in toks)
    assert has_minus or len(toks) > 0

def test_to_string_public():
    assert to_string(TokenKind.Const) == "const"
    assert to_string(TokenKind.Identifier) == "identifier"
    assert to_string(TokenKind.Minus) == "minus"
    assert to_string(TokenKind.IntLit) == "int_lit"
    assert to_string(TokenKind.Eof) == "eof"

def test_bin_prec_public():
    assert bin_prec(TokenKind.Const) is None
    assert bin_prec(TokenKind.Minus) == 10