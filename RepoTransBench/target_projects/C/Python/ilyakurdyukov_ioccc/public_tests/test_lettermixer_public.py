import os

import pytest

from src.lettermixer import lettermixer

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), '../tests/2020-lettermixer')

@pytest.mark.parametrize("filename", [
    "public_test_alpha.txt",
    "public_test_unicode.txt",
    "public_test_punctuation.txt",
])
def test_lettermixer_public(filename):
    input_path = os.path.join(TESTDATA_DIR, filename)
    with open(input_path, encoding='utf-8') as f:
        input_data = f.read()
    output = lettermixer(input_data)
    assert output is not None
    assert isinstance(output, str)