import pytest

from homu import utils as utils_mod

def test_alphanumeric_only_public():
    assert utils_mod.alphanumeric_only("xyz789GH@#!") == "xyz789GH"
    assert utils_mod.alphanumeric_only(" **&$  321 ") == "321"