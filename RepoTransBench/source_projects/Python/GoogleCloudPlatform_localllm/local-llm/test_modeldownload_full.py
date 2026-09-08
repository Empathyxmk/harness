import sys
import types
import importlib
import pytest
from unittest.mock import patch, MagicMock

modeldownload = importlib.import_module("modeldownload")
modelfiles = importlib.import_module("modelfiles")

def test_default_filename_valid(monkeypatch):
    # Should produce expected filename format
    monkeypatch.setattr(modelfiles, "DEFAULT_FILE_EXT", "gguf")
    repo_id = "TheBloke/foo-123-gguf"
    result = modeldownload.default_filename(repo_id)
    assert result == "foo-123.Q4_K_M.gguf"

def test_default_filename_invalid(monkeypatch):
    bad_repo = "broken"
    assert modeldownload.default_filename(bad_repo) == ""
    # Wrong file ending
    repo_bad = "foo/bar-model"
    monkeypatch.setattr(modelfiles, "DEFAULT_FILE_EXT", "ggufx")
    assert modeldownload.default_filename(repo_bad) == ""
    # Not ending in gguf
    monkeypatch.setattr(modelfiles, "DEFAULT_FILE_EXT", "gguf")
    assert modeldownload.default_filename("foo/bar-model-xyz") == ""

def test_download_calls_hf_hub_download(monkeypatch):
    mock = MagicMock(return_value="downloaded_path")
    monkeypatch.setattr("huggingface_hub.hf_hub_download", mock)
    assert modeldownload.download("foo", "bar") == "downloaded_path"
    mock.assert_called_with(repo_id="foo", filename="bar")

def test_remove_file(monkeypatch):
    repo_id = "foo/bar"
    filename = "model.gguf"
    # Simulate path_from_model returning a file path;
    # will test with os.remove called
    blob_path = "/somewhere/model.gguf"
    monkeypatch.setattr(modelfiles, "path_from_model", lambda a, b: blob_path)
    monkeypatch.setattr("os.path.realpath", lambda x: x + "_real")
    rm_called = []
    monkeypatch.setattr("os.remove", lambda x: rm_called.append(x))
    monkeypatch.setattr("os.path.isfile", lambda x: True)
    # Remove should call os.remove twice
    modeldownload.remove(repo_id, filename)
    assert blob_path in rm_called

def test_remove_file_not_found(monkeypatch):
    # Simulate not found conditions
    repo_id = "foo/bar"
    filename = "model.gguf"
    monkeypatch.setattr(modelfiles, "path_from_model", lambda a, b: None)
    monkeypatch.setattr("os.path.realpath", lambda x: x)
    monkeypatch.setattr("os.remove", lambda x: (_ for _ in ()).throw(FileNotFoundError()))
    monkeypatch.setattr("os.path.isfile", lambda x: False)
    # Should not raise
    assert modeldownload.remove(repo_id, filename) is None

def test_remove_repo(monkeypatch):
    repo_id = "foo/bar"
    monkeypatch.setattr(modelfiles, "path_from_model", lambda a, b: None)
    monkeypatch.setattr(modelfiles, "path_from_repo", lambda r: "/repo/" + r if r else "")
    rm_tree = []
    monkeypatch.setattr("shutil.rmtree", lambda p: rm_tree.append(p))
    ret = modeldownload.remove(repo_id, "")
    assert ret.startswith("/repo/")

def test_remove_repo_none(monkeypatch):
    repo_id = "foo/bar"
    monkeypatch.setattr(modelfiles, "path_from_model", lambda a, b: None)
    monkeypatch.setattr(modelfiles, "path_from_repo", lambda r: "")
    monkeypatch.setattr("shutil.rmtree", lambda p: p)
    assert modeldownload.remove(repo_id, "") == ""