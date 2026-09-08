import sys
import os
import subprocess
import shlex

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def run_cli_args(args):
    shortuuid_py = os.path.join(os.path.dirname(__file__), "..", "shortuuid", "cli.py")
    cmd = f"{sys.executable} {shlex.quote(shortuuid_py)} {' '.join(map(shlex.quote, args))}"
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True
    )
    out, err = proc.communicate()
    return out, err

def test_public_cli_invalid_command():
    out, err = run_cli_args(["notacommand"])
    text = (out + err).lower()
    assert "invalid" in text or "unknown" in text or "unrecognized" in text

def test_public_cli_decode_bad_string():
    # Give an invalid string to decode and expect an error message
    out, err = run_cli_args(["decode", "333BADSHORTuuid!"])
    text = (out + err).lower()
    assert "error" in text or "invalid" in text or text.strip() == ""

def test_public_cli_encoding_too_few_args():
    out, err = run_cli_args(["encode"])
    text = (out + err).lower()
    assert "usage" in text or "argument" in text or "error" in text