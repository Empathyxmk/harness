"""Public tests for latexify.ast_utils using different AST input."""

import ast
import pytest

import src.latexify.ast_utils as ast_utils


def test_public_ast_body_to_expr():
    # Different test: sum of two different numbers
    node = ast.parse("y = 4 + 8")
    expr = ast_utils.body_to_expr(node.body[0])
    assert isinstance(expr, ast.BinOp)
    assert isinstance(expr.op, ast.Add)
    assert isinstance(expr.left, ast.Constant)
    assert isinstance(expr.right, ast.Constant)
    assert expr.left.value == 4
    assert expr.right.value == 8


def test_public_ast_is_simple_return():
    node1 = ast.parse("def f():\n    return 'abc'").body[0]
    node2 = ast.parse("def g():\n    x = 3\n    return x").body[0]
    assert ast_utils.is_simple_return(node1)
    assert not ast_utils.is_simple_return(node2)


def test_public_ast_maybe_strip_expr_wrapping():
    expr_ast = ast.parse("1 + 2", mode="eval")
    res = ast_utils.maybe_strip_expr_wrapping(expr_ast)
    assert isinstance(res, ast.Expression)
    stmt_ast = ast.parse("a = 3", mode="exec")
    res2 = ast_utils.maybe_strip_expr_wrapping(stmt_ast)
    assert isinstance(res2, ast.Module)