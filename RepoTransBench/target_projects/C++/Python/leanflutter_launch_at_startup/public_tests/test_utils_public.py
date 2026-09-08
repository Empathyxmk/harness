import pytest

def test_utils_sanity_public_basic():
    # This test checks basic arithmetic, mapping from C++: EXPECT_EQ(1 + 1, 2);
    assert 1 + 1 == 2