import pytest
from src.load_aurora import load_aurora

def test_load_aurora_nonexistent_datafile():
    try:
        out = load_aurora('non_existent_file.something')
        assert out is None or not out or out == []
    except Exception:
        assert True

def test_load_aurora_no_args():
    with pytest.raises(TypeError):
        load_aurora()