import pytest
from src.lipsdp.error_messages import invalid_mode

def test_message():
    with pytest.raises(ValueError) as e:
        invalid_mode('foobar')
    assert 'formulation must be in' in str(e.value)