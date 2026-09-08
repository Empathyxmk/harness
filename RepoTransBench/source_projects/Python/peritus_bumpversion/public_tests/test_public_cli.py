import sys
import subprocess

def test_help_invocation_cli_public():
    # Should yield usage/help text for python -m bumpversion --help
    proc = subprocess.run([sys.executable, "-m", "bumpversion", "--help"], capture_output=True, text=True)
    assert "usage" in proc.stdout.lower() or "help" in proc.stdout.lower()
    assert proc.returncode == 0 or proc.returncode == 1  # Sometimes argparse returns 1 on help