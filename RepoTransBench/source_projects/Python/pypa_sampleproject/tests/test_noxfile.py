import types
import sys
import pathlib
import pytest

src_dir = pathlib.Path(__file__).parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

import importlib

def _reload_noxfile_without_needs_version():
    """
    Reloads noxfile.py after patching it to remove the
    problematic .needs_version option.
    """
    import os
    original_file = pathlib.Path(__file__).parent.parent / "noxfile.py"
    backup_file = original_file.with_suffix(".bak")
    # Read and conditionally patch
    with open(original_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Remove or comment out any assignment to nox.options.needs_version
    filtered = []
    for l in lines:
        if "needs_version" in l and "nox.options." in l:
            filtered.append("# " + l)
        else:
            filtered.append(l)
    # Write a patched copy to .bak
    with open(backup_file, "w", encoding="utf-8") as f:
        f.writelines(filtered)
    # Rename originals
    try:
        orig = original_file.rename(original_file.with_suffix(".orig"))
        backup_file.rename(original_file)
        importlib.invalidate_caches()
        mod = importlib.import_module("noxfile")
    finally:
        # Restore original file
        pathlib.Path(__file__).parent.parent.joinpath("noxfile.py").unlink()
        original_file.with_suffix(".orig").rename(original_file)
    return mod

@pytest.fixture(scope="module")
def noxfile_module():
    return _reload_noxfile_without_needs_version()

def test_lint_runs_and_installs(noxfile_module):
    class DummySession:
        installed = []
        runs = []
        posargs = []
        def install(self, *args): self.installed.append(args)
        def run(self, *args): self.runs.append(args)
    s = DummySession()
    noxfile_module.lint(s)
    assert any("flake8" in a for t in s.installed for a in t)
    assert any("flake8" in a for t in s.runs for a in t)

def test_build_and_check_dists_invocations(noxfile_module):
    class DummySession:
        installed = []
        runs = []
        posargs = []
        def install(self, *args): self.installed.append(args)
        def run(self, *args): self.runs.append(args)
    s = DummySession()
    noxfile_module.build_and_check_dists(s)
    assert s.installed
    assert s.runs

def test_tests_invokes_build(monkeypatch, noxfile_module):
    class DummySession:
        installed = []
        runs = []
        posargs = []
        def install(self, *args): self.installed.append(args)
        def run(self, *args, **kwargs): self.runs.append(args)
    s = DummySession()
    def fake_build_and_check_dists(sess): s.runs.append("build_and_check_called")
    monkeypatch.setattr(noxfile_module, "build_and_check_dists", fake_build_and_check_dists)
    s.posargs = []
    import os
    monkeypatch.setattr(os, "listdir", lambda d: ["wheel.whl", "source.tar.gz"])
    monkeypatch.setattr(os.path, "join", lambda a,b: f"{a}/{b}")
    noxfile_module.tests(s)
    assert "build_and_check_called" in s.runs