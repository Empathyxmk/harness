import os
import json
import pytest

from src.jsonstream import jsonstream

@pytest.mark.skip(reason="Requires actual JSONStream implementation with streaming parsing and event interface")
def test_parse_package_json_stream():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'package.json'))
    with open(file_path, encoding='utf-8') as f:
        expected = json.load(f)

    parser = jsonstream.parse([])

    called = 0

    # Simulate streamed parsing
    for data in parser.parse_file(file_path):  # Should yield full file as object
        called += 1
        assert data == expected

    assert called == 1