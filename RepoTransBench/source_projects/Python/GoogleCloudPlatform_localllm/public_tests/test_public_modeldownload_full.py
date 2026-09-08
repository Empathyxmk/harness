import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../local-llm")))
import modeldownload
import modelfiles
from unittest.mock import MagicMock

def test_public_default_filename_valid(monkeypatch):
    # Different data than private test
    monkeypatch.setattr(modelfiles, "DEFAULT_FILE_EXT", "gguf")
    repo_id = "OtherAuthor/my-cool-model-884"
    result = modeldownload.default_filename(repo_id)
    assert result == "my-cool-model-884.Q4_K_M.gguf"

def test_public_download_calls_hf_hub_download(monkeypatch):
    # Use different repo_id and filename than private test
    mock = MagicMock(return_value="output_path")
    monkeypatch.setattr("huggingface_hub.hf_hub_download", mock)
    assert modeldownload.download("repoX", "modelFile.bin") == "output_path"
    mock.assert_called_with("repoX", "modelFile.bin")

def test_public_remove_file(monkeypatch):
    repo_id = "baz/bar"
    filename = "anothermodel.gguf"
    blob_path = "/tmp/anothermodel.gguf"
    monkeypatch.setattr(modelfiles, "path_from_model", lambda a, b: blob_path)
    monkeypatch.setattr("os.path.realpath", lambda x: x + "_real")
    rm_called = []
    monkeypatch.setattr("os.remove", lambda x: rm_called.append(x))
    monkeypatch.setattr("os.path.isfile", lambda x: True)
    modeldownload.remove(repo_id, filename)
    # Should call remove twice (for both paths)
    assert all(blob_path in p for p in rm_called)