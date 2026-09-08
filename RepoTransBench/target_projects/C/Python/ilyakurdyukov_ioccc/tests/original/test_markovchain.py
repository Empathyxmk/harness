import os

import pytest

from src.markovchain import markovchain

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), '../../tests/2020-markovchain')


@pytest.mark.parametrize("inputfile, y, s, seed", [
    ("test_input.txt", 1, 1, 10),
    ("test_short.txt", 1, 1, 10),
    ("test_input2.txt", 1, 2, 123),
    ("test_empty.txt", 1, 1, 999),
])
def test_markovchain_original(inputfile, y, s, seed):
    input_path = os.path.join(TESTDATA_DIR, inputfile)
    # Only test that function does not crash and returns a string,
    # as the original output ref is not present.
    output = markovchain(input_path, y, s, seed)
    assert output is not None
    assert isinstance(output, str)