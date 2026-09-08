import pytest
from src.lipsdp.error_messages import cap_input, invalid_mode

def test_cap_input_under_limit(capsys):
    output = cap_input(2, 3, 'randomly chosen neurons')
    assert output == 2
    captured = capsys.readouterr()
    assert captured.out == ""

def test_cap_input_at_limit(capsys):
    limit = 6
    output = cap_input(limit, 4, 'decision variables')
    assert output == limit
    captured = capsys.readouterr()
    assert captured.out == ""

def test_cap_input_over_limit(capsys):
    # 4 choose 2 = 6
    result = cap_input(20, 4, 'decision variables')
    assert result == 6
    captured = capsys.readouterr()
    assert "was capped" in captured.out

def test_invalid_mode():
    with pytest.raises(ValueError):
        invalid_mode('badformulation')