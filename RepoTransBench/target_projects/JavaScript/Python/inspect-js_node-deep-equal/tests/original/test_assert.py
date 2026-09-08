import pytest
from src.assert_util import assert_

def test_assert_simple_assertion():
    # Should not throw
    assert_(True, 'Should not throw')

def test_assert_assertion_throws_on_false():
    with pytest.raises(AssertionError) as excinfo:
        assert_(False, 'Should throw')
    assert str(excinfo.value) == 'Should throw'