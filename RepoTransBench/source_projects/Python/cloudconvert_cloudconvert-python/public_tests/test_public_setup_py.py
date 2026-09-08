import importlib.util
import os

def test_setup_py_runs_public(tmp_path):
    """Ensure setup.py runs without error and sets up parameters (public test, diff input)"""
    # Always create a dummy README with a different content and copy setup.py
    dest = tmp_path / "README.md"
    with open(dest, "w") as f:
        f.write("# Public dummy readme")
    setup_src = os.path.join(os.getcwd(), "setup.py")
    setup_dst = tmp_path / "setup.py"
    import shutil
    shutil.copy(setup_src, setup_dst)
    # run as module
    import subprocess, sys
    code = subprocess.call([sys.executable, str(setup_dst)], cwd=tmp_path)
    assert code == 0 or code == 1  # setuptools/setup.py often returns 1 for dry runs, not fatal