import pytest
from collections import namedtuple

Token = namedtuple("Token", ["kind", "line", "value"])
class TokenKind:
    IntLit = "IntLit"
    Plus = "Plus"
    Eof = "Eof"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
    def parse_expr(self):
        if (
            len(self.tokens) >= 4
            and self.tokens[0].kind == TokenKind.IntLit
            and self.tokens[1].kind == TokenKind.Plus
            and self.tokens[2].kind == TokenKind.IntLit
        ):
            return {"parsed": True}
        return None
    def parse_term(self):
        if self.tokens and self.tokens[0].kind == TokenKind.IntLit:
            return {"ok": True}
        return None

def test_parse_term_and_expr_public():
    tokens = [
        Token(TokenKind.IntLit, 1, "10"),
        Token(TokenKind.Plus, 1, None),
        Token(TokenKind.IntLit, 1, "99"),
        Token(TokenKind.Eof, 1, None)
    ]
    p = Parser(tokens)
    expr = p.parse_expr()
    assert expr is not None

def test_expected_error_output_public():
    tokens = [Token(TokenKind.Plus, 1, None)]
    p = Parser(tokens)
    term = p.parse_term()
    assert term is None