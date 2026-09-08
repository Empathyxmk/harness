# Patch import so the 'coqtop' module is found by pytest.
import sys
import os
sys.path.insert(0, os.path.abspath('python'))
import pytest

from coqtop import Coqtop, CoqtopError

def test_coqtop_basic_init():
    c = Coqtop()
    assert isinstance(c, Coqtop)
    assert hasattr(c, "states")

def test_coqtop_error_str():
    err = CoqtopError("fail")
    assert "fail" in str(err)

def test_coqtop_join_not_empty():
    import coqtop
    sms = ["a", "", "b", ""]
    result = coqtop.join_not_empty(sms, ";")
    assert result == "a;b"

def test_coqtop_is_in_valid_dune_project_false():
    c = Coqtop()
    c.xml = None
    assert not c.is_in_valid_dune_project("fakefile.v")

# Remove the test that calls c.reset() since Coqtop.reset() does not exist and led to AttributeError
# This avoids the test failure and preserves the valid coverage-increasing tests.