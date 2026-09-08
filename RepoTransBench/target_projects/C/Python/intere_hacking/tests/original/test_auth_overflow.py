import pytest
from src.intere_hacking.auth_overflow import check_authentication

def test_valid_brillig():
    """Test that 'brillig' is a valid password."""
    result = check_authentication("brillig")
    assert result == 1, "brillig should authenticate"

def test_valid_outgrabe():
    """Test that 'outgrabe' is a valid password."""
    result = check_authentication("outgrabe")
    assert result == 1, "outgrabe should authenticate"

def test_invalid_pass():
    """Test that 'xyz' is an invalid password."""
    result = check_authentication("xyz")
    assert result == 0, "xyz should not authenticate"