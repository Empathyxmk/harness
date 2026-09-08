import os
import sys
import tempfile
import types
import pytest

# Patch huggingface_hub.constants for test isolation
import importlib
from unittest import mock

modelfiles = importlib.import_module("modelfiles")

@pytest.fixture(autouse=True)
def patch_constants(monkeypatch, tmp_path):
    constant_mod = importlib.import_module("huggingface_hub.constants")
    monkeypatch.setattr(constant_mod, "HF_HUB_CACHE", str(tmp_path / "hubcache"))
    monkeypatch.setattr(modelfiles, "constants", constant_mod)


def create_fake_model_dir(tmp_path, repo="foo/bar", model="bar.Q4_K_M.gguf"):
    parts = repo.split("/")
    repo_dir = tmp_path / "hubcache" / "--".join(["models", parts[0], parts[1]])
    repo_dir.mkdir(parents=True, exist_ok=True)
    model_path = repo_dir / model
    model_path.write_text("fake model")
    return model_path

def test_get_model_dir_patched(tmp_path):
    # Should return the patched hub cache
    assert str(tmp_path / "hubcache") in modelfiles.get_model_dir()

def test_list_models(tmp_path, monkeypatch):
    # No dir present
    monkeypatch.setattr(modelfiles, "get_model_dir", lambda : str(tmp_path / "notfound"))
    assert modelfiles.list_models() == []

    # Dir present, find gguf files
    model_file = create_fake_model_dir(tmp_path)
    monkeypatch.setattr(modelfiles, "get_model_dir", lambda : str(tmp_path / "hubcache"))
    files = modelfiles.get_all_files(os.path.dirname(os.path.dirname(model_file)))
    filtered = modelfiles.filter_models(files)
    assert len(filtered) >= 1
    # Should be found in list_models as well
    assert filtered == modelfiles.list_models()

def test_filter_models_and_model_from_path():
    files = [
        "/some/fake/path/models--foo--bar/baz.Q4_K_M.gguf",
        "/some/other/path/notamodel.txt"
    ]
    filtered = modelfiles.filter_models(files)
    assert isinstance(filtered, list)
    assert all(isinstance(tup, tuple) and len(tup) == 2 for tup in filtered)

def test_model_from_path_variants():
    # Standard repo path
    p = "something/models--foo--bar/baz.Q4_K_M.gguf"
    repo, model = modelfiles.model_from_path(p)
    assert repo == "foo/bar"
    assert model == "baz.Q4_K_M.gguf"

    # Malformed paths
    assert modelfiles.model_from_path("no-model-here") == ("", "")

def test_path_from_repo(tmp_path, monkeypatch):
    monkeypatch.setattr(modelfiles, "get_model_dir", lambda : str(tmp_path / "hubcache"))
    # Valid repo
    rv = modelfiles.path_from_repo("foo/bar")
    assert "models--foo--bar" in rv
    # Invalid repo
    assert modelfiles.path_from_repo("foo") == ""

def test_get_all_files(tmp_path):
    fn = create_fake_model_dir(tmp_path)
    out = modelfiles.get_all_files(str(fn.parent.parent))
    assert any(f.endswith(".gguf") for f in out)
    # Empty dir
    empty = tmp_path / "empty"
    empty.mkdir()
    assert modelfiles.get_all_files(str(empty)) == []

def test_path_from_model(tmp_path, monkeypatch):
    fn = create_fake_model_dir(tmp_path)
    repo_id = "foo/bar"
    model = os.path.basename(fn)
    monkeypatch.setattr(modelfiles, "get_model_dir", lambda : str(tmp_path / "hubcache"))
    # Produces valid model path
    out = modelfiles.path_from_model(repo_id, model)
    assert out and out.endswith(model)
    # Model not found
    assert modelfiles.path_from_model("foo/bar", "notfound.model") is None

def test_find_model():
    files = [
        "/root/test/1.Q4_K_M.gguf",
        "/root/test/2.Q4_K_M.gguf",
    ]
    found = modelfiles.find_model(files, "1.Q4_K_M.gguf")
    assert found.endswith("1.Q4_K_M.gguf")
    assert modelfiles.find_model(files, "X.Q4_K_M.gguf") is None