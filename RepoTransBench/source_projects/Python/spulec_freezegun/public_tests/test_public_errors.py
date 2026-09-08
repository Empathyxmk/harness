import pytest

def test_public_raises_type_error():
    with pytest.raises(TypeError):
        int("notanumber")

def test_public_raises_value_error():
    with pytest.raises(ValueError):
        float("NaNnot")