"""Public tests for latexify.analyzers with different ASTs."""

import ast
import src.latexify.analyzers as analyzers

def test_public_enumerate_assignments():
    code = """
x = 1
y = x + 2
return y
"""
    tree = ast.parse(code)
    assigns = list(analyzers.enumerate_assignments(tree))
    assert len(assigns) == 2
    assert assigns[0].targets[0].id == "x"
    assert assigns[1].targets[0].id == "y"

def test_public_contains_tuple_unpack():
    code = "a, b, c = 1, 2, 3"
    tree = ast.parse(code)
    # Not present in a simple assignment
    assert analyzers.contains_tuple_unpack(tree)

    code2 = "d = 4"
    tree2 = ast.parse(code2)
    assert not analyzers.contains_tuple_unpack(tree2)