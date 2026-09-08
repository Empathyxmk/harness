import pytest

from homu import main as main_mod

def test_pr_body_contains_diff_key():
    body = "Closes #99\nExtra: refactor code"
    assert main_mod.pr_body_contains(body, "refactor")

def test_pr_body_not_contains_diff_key():
    body = "Implements feature X.\nNone found."
    assert not main_mod.pr_body_contains(body, "security")