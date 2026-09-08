import pytest
from src.generation_procedure import generation_procedure, GenerationProcedureError
import numpy as np

def test_basic_generation_procedure():
    challenge_size = 32
    challenge = np.random.randint(0, 2, challenge_size).tolist()
    response, helper_data = generation_procedure(challenge)
    assert response is not None and not isinstance(response, type(None))
    assert isinstance(response, list)
    assert all(bit in [0, 1] for bit in response)
    assert helper_data
    assert isinstance(helper_data, dict)

def test_generation_with_different_challenge_sizes():
    challenge_sizes = [24, 80, 200]
    for current_size in challenge_sizes:
        challenge = np.random.randint(0, 2, current_size).tolist()
        response, helper_data = generation_procedure(challenge)
        assert response is not None and not isinstance(response, type(None))
        assert isinstance(response, list)
        assert all(bit in [0, 1] for bit in response)
        assert helper_data
        assert isinstance(helper_data, dict)

def test_empty_challenge():
    with pytest.raises(GenerationProcedureError):
        generation_procedure([])