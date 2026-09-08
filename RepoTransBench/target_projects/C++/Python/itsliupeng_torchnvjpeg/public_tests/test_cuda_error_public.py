import pytest

def simulate_cuda_error(code):
    if code == 456:
        raise RuntimeError("CUDA error code 456")
    if code == 789:
        raise RuntimeError("CUDA error code 789")

def test_simulate_cuda_error_456():
    with pytest.raises(RuntimeError):
        simulate_cuda_error(456)

def test_simulate_cuda_error_789():
    try:
        simulate_cuda_error(789)
        assert False, "Should have raised RuntimeError"
    except RuntimeError as e:
        assert "789" in str(e)