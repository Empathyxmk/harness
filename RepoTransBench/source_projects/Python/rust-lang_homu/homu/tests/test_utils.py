import pytest

from homu import utils as utils_mod

def test_alphanumeric_only_cases():
    assert utils_mod.alphanumeric_only("abc123DEF!@#") == "abc123DEF"
    assert utils_mod.alphanumeric_only(" **&$  456 ") == "456"