import pytest
import numpy as np
from src.generation_procedure import generation_procedure
from src.reproduction_procedure import reproduction_procedure

def test_reproduction_consistency():
    challenge_size = 32
    challenge = np.random.randint(0, 2, challenge_size).tolist()
    expected_response, helper_data = generation_procedure(challenge)
    reproduced_response = reproduction_procedure(challenge, helper_data)
    assert reproduced_response is not None
    assert isinstance(reproduced_response, list)
    assert all(bit in [0, 1] for bit in reproduced_response)
    assert reproduced_response == expected_response

def test_reproduction_with_different_challenge_sizes():
    challenge_sizes = [24, 80, 200]
    for current_size in challenge_sizes:
        challenge = np.random.randint(0, 2, current_size).tolist()
        expected_response, helper_data = generation_procedure(challenge)
        reproduced_response = reproduction_procedure(challenge, helper_data)
        assert reproduced_response == expected_response