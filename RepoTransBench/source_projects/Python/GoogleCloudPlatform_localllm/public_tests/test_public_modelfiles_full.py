import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../local-llm")))
import modelfiles

def test_public_find_llmfiles(monkeypatch):
    # Use a different dir and files than private test
    test_dir = "/tmp/some-llm-model-dir"
    test_files = ["lion.Q4_0.gguf", "giraffe.Q8_0.gguf"]
    monkeypatch.setattr("os.listdir", lambda _: test_files)
    monkeypatch.setattr("os.path.isdir", lambda x: x == test_dir)
    monkeypatch.setattr("os.path.join", os.path.join)
    output = modelfiles.find_llmfiles(test_dir)
    assert any(f.endswith(".gguf") for f in output)
    assert "lion.Q4_0.gguf" in ''.join(output)

def test_public_is_llmfile():
    assert modelfiles.is_llmfile("rhino.Q7_0.gguf")
    assert not modelfiles.is_llmfile("zebra.txt")