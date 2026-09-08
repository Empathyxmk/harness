import sys
import os
import pytest

# Add the local-llm directory to sys.path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../local-llm")))
import modeldownload

def test_public_default_filename():
    # Different repo id than private test
    repo_id = "SomeAuthor/Mistral-Medium-AI-GGUF"
    filename = modeldownload.default_filename(repo_id)
    assert filename.lower().endswith(".gguf")
    assert "mistral-medium" in filename.lower()

def test_public_default_filename_lowercase():
    repo_id = "anotherone/gpt-foo-gguf"
    filename = modeldownload.default_filename(repo_id)
    assert filename.lower().endswith(".gguf")
    assert "gpt-foo" in filename.lower()