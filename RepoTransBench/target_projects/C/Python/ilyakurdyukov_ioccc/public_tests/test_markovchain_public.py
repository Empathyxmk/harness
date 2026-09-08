import os

import pytest

from src.markovchain import markovchain

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), '../tests/2020-markovchain')

@pytest.mark.parametrize("filename, y, s, seed", [
    ("public_test_input_A.txt", 1, 1, 555),
    ("public_test_input_B.txt", 1, 2, 333),
    ("public_test_empty.txt", 1, 1, 12345),
])
def test_markovchain_public(filename, y, s, seed):
    input_path = os.path.join(TESTDATA_DIR, filename)
    output = markovchain(input_path, y, s, seed)
    assert output is not None
    assert isinstance(output, str)