import os
import sys
import pytest

from src import includepaths

def test_includepaths_runs(tmp_path, monkeypatch):
    # Simulate running includepaths in a test, ensuring Algorithms folder is checked.
    # Ensure test is run from repo root

    # Create the Algorithms directory if not exists for test isolation
    root = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(root, '..', '..'))
    algorithms_dir = os.path.join(repo_root, "Algorithms")
    os.makedirs(algorithms_dir, exist_ok=True)
    monkeypatch.chdir(os.path.dirname(os.path.abspath(includepaths.__file__)))
    try:
        alg = includepaths.includepaths()
        assert os.path.isdir(alg)
        assert "Algorithms" in alg
        # cleanup sys.path
        if alg in sys.path:
            sys.path.remove(alg)
    finally:
        pass  # intentionally let Algorithms remain for reuse by other tests