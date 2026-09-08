import pytest
import numpy as np
from src.generation_procedure import generation_procedure
from src.reproduction_procedure import reproduction_procedure, ReproductionProcedureError

def test_reproduction_consistency():
    challenge_size = 64
    challenge = np.random.randint(0, 2, challenge_size).tolist()
    expected_response, helper_data = generation_procedure(challenge)
    reproduced_response = reproduction_procedure(challenge, helper_data)
    assert reproduced_response is not None
    assert isinstance(reproduced_response, list)
    assert all(bit in [0, 1] for bit in reproduced_response)
    assert reproduced_response == expected_response

def test_reproduction_with_different_challenge_sizes():
    challenge_sizes = [16, 128, 256]
    for current_size in challenge_sizes:
        challenge = np.random.randint(0, 2, current_size).tolist()
        expected_response, helper_data = generation_procedure(challenge)
        reproduced_response = reproduction_procedure(challenge, helper_data)
        assert reproduced_response == expected_response

def test_invalid_helper_data():
    challenge_size = 64
    challenge = np.random.randint(0, 2, challenge_size).tolist()

    # Empty helper data
    out = reproduction_procedure(challenge, {})
    assert out == []

    # Invalid helper data type
    out = reproduction_procedure(challenge, 123)
    assert out == []

def test_challenge_mismatch():
    challenge_size = 64
    challenge1 = np.random.randint(0, 2, challenge_size).tolist()
    challenge2 = np.random.randint(0, 2, challenge_size).tolist()
    _, helper_data = generation_procedure(challenge1)
    out1 = reproduction_procedure(challenge1, helper_data)
    out2 = reproduction_procedure(challenge2, helper_data)
    assert out1 != out2