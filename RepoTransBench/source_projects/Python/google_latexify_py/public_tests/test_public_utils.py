"""Public tests for utilities."""

import ast
import sys

import src.latexify.test_utils as test_utils


def test_require_at_least_decorator():
    called = {"value": False}

    @test_utils.require_at_least(0)
    def f():
        called["value"] = True

    f()
    assert called["value"] is True

    # Should NOT call on higher minor required than running interpreter
    called = {"value": False}

    @test_utils.require_at_least(sys.version_info.minor + 1)
    def f2():
        called["value"] = True

    f2()
    assert called["value"] is False


def test_require_at_most_decorator():
    called = {"value": False}

    @test_utils.require_at_most(100)
    def f():
        called["value"] = True

    f()
    assert called["value"] is True

    called = {"value": False}

    @test_utils.require_at_most(sys.version_info.minor - 1)
    def f2():
        called["value"] = True

    f2()
    assert called["value"] is False


def test_ast_equal_and_assert_ast_equal_simple():
    observed = ast.parse("b = 3\n", mode="exec")
    expected = ast.parse("b = 3", mode="exec")
    assert test_utils.ast_equal(observed, expected)
    test_utils.assert_ast_equal(observed, expected)


def test_ast_equal_and_assert_ast_equal_expr():
    observed = ast.parse("x + 2", mode="eval")
    expected = ast.parse("x + 2", mode="eval")
    assert test_utils.ast_equal(observed, expected)
    test_utils.assert_ast_equal(observed, expected)