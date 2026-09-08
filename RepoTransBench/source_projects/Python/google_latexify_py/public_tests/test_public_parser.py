"""Public tests for latexify.parser with new code snippets."""

import src.latexify.parser as parser


def test_parse_signature_public():
    sig = parser.parse_signature("def foo(a: float, y) -> int: ...")
    assert sig.name == "foo"
    assert [a.arg for a in sig.args.args] == ["a", "y"]
    assert sig.returns.id == "int"


def test_parse_assignment_public():
    node = parser.parse_assignment("z = 12")
    assert node.targets[0].id == "z"
    assert getattr(node.value, "value", None) == 12