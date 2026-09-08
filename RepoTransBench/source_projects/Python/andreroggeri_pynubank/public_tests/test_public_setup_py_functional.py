import subprocess
import sys

def test_setup_py_runs_public():
    # Use a dummy command to ensure setup.py is functional with a different command
    result = subprocess.run([sys.executable, "setup.py", "--name"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # This should return a non-empty project name
    out = result.stdout.decode()
    assert "pynubank" in out.lower()

def test_setup_py_metadata_public():
    result = subprocess.run([sys.executable, "setup.py", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Version should be numbers and dots
    version = result.stdout.decode().strip()
    # Check for digits and dots but do not require specific version
    assert version.replace('.', '').isdigit()