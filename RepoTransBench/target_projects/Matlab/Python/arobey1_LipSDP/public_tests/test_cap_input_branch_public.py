import pytest
from src.lipsdp.error_messages import cap_input

def test_cap_input_lower_and_upper_public(capsys):
    capped1 = cap_input(11, 10, 'neurons')
    assert capped1 == 10
    out1 = capsys.readouterr().out
    assert 'was capped' in out1

    capped2 = cap_input(10, 10, 'neurons')
    assert capped2 == 10
    out2 = capsys.readouterr().out
    assert out2 == ""

    capped3 = cap_input(7, 10, 'neurons')
    assert capped3 == 7
    out3 = capsys.readouterr().out
    assert out3 == ""

    with pytest.raises(ValueError):
        cap_input(-2, 10, 'neurons')