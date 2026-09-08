import pytest

from homu import main as main_mod

def test_pr_body_contains():
    body = "Closes #42\nFixes issues"
    assert main_mod.pr_body_contains(body, "Fixes")
    assert not main_mod.pr_body_contains(body, "missing")