from shshsh.quick import _pipe_run_return
import pytest

def test_public_pipe_return_type():
    # Instead of cmd 'ls', use 'echo'
    ret = _pipe_run_return(["echo", "testval"])
    assert hasattr(ret, "stdout")

def test_public_pipe_invalid():
    with pytest.raises(Exception):
        _pipe_run_return(["nonexistent_command_for_public"])