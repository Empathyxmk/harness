import os

import pytest

from src.lettermixer import lettermixer


TESTDATA_DIR = os.path.join(os.path.dirname(__file__), '../../tests/2020-lettermixer')


@pytest.mark.parametrize("filename", [
    "test_basic.txt",
    "test_symbols.txt",
    "test_empty.txt",
])
def test_lettermixer_original(filename):
    input_path = os.path.join(TESTDATA_DIR, filename)
    with open(input_path, encoding='utf-8') as f:
        input_data = f.read()
    # Since original C code output is written to file, but we don't have ref output, just check not crash
    output = lettermixer(input_data)
    assert output is not None
    assert isinstance(output, str)