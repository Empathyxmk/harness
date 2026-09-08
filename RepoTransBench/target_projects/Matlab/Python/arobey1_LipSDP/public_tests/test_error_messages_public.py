import pytest
from src.lipsdp.error_messages import cap_input, invalid_mode

def test_error_strings_public(capsys):
    # cap_input should print 'was capped'
    cap_input(6, 5, 'neurons')
    out = capsys.readouterr().out
    assert 'was capped' in out

    with pytest.raises(ValueError) as exc:
        invalid_mode('strange-mode')
    assert 'formulation must be in' in str(exc.value)