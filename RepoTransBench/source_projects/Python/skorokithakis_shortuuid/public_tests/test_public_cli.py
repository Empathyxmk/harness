import sys
import os
import subprocess
import shlex

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_cli_args(args):
    """
    Run the shortuuid CLI as a subprocess.
    """
    shortuuid_py = os.path.join(os.path.dirname(__file__), "..", "shortuuid", "cli.py")
    cmd = f"{sys.executable} {shlex.quote(shortuuid_py)} {' '.join(map(shlex.quote, args))}"
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True
    )
    out, err = proc.communicate()
    return out, err

def test_cli_basic_output():
    out, err = run_cli_args(["generate"])
    val = out.strip()
    assert val, f"CLI did not output anything: stdout={out!r}, stderr={err!r}"

def test_cli_with_length():
    out, err = run_cli_args(["generate", "--length", "19"])
    val = out.strip()
    assert len(val) == 19

def test_cli_help():
    out, err = run_cli_args(["--help"])
    # Should get usage message in out or err
    found = ("usage:" in out.lower()) or ("usage:" in err.lower())
    assert found, f"No usage message found. Out: {out} Err: {err}"