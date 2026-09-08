import pytest

def is_supported_subsampling_ratio(ratio):
    # Dummy implementation: supports only 221 and 222
    return ratio == 221 or ratio == 222

def test_support_221():
    assert is_supported_subsampling_ratio(221)

def test_not_support_223():
    assert not is_supported_subsampling_ratio(223)