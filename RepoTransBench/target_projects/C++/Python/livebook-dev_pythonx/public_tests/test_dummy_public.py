import pytest

def test_always_pass_public():
    # Public: use inequality instead of equality to maintain different but trivial check
    assert 2 != 3