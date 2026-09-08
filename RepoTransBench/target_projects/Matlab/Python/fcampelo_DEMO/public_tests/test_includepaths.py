import os
import sys
import pytest

from src import includepaths

def test_public_includepaths_runs(tmp_path, monkeypatch):
    # Simulate different path handling, check Algorithms in sys.path
    root = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(root, '..'))
    algorithms_dir = os.path.join(repo_root, "Algorithms")
    os.makedirs(algorithms_dir, exist_ok=True)
    monkeypatch.chdir(os.path.dirname(os.path.abspath(includepaths.__file__)))
    alg = includepaths.includepaths()
    assert os.path.isdir(alg)
    is_alg_added = any('Algorithms' in p for p in sys.path)
    assert is_alg_added
    if alg in sys.path:
        sys.path.remove(alg)