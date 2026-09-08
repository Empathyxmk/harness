import os
import subprocess

def bin_path():
    here = os.path.abspath(os.path.dirname(__file__))
    root = os.path.abspath(os.path.join(here, ".."))
    path = os.path.join(root, "bin", "cdklocal")
    assert os.path.exists(path), f"cdklocal CLI not found at: {path}"
    return path

def run_cdklocal_cli(*args):
    script_path = bin_path()
    if not os.access(script_path, os.X_OK):
        os.chmod(script_path, 0o755)
    proc = subprocess.run(
        [script_path] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr

def test_cdklocal_cli_help_public():
    code, out, err = run_cdklocal_cli("--help")
    assert code == 0
    text = out + err
    assert "usage" in text.lower()