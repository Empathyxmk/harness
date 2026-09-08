import subprocess
import sys

def test_s3_pit_restore_version_public():
    """Check output for the --version argument (should exit code 2 and mention missing bucket as before)"""
    result = subprocess.run(
        [sys.executable, "s3-pit-restore", "-V"], capture_output=True, encoding="utf-8"
    )
    # Still expects missing-bucket behavior, but using -V instead of --version
    assert result.returncode == 2
    assert ("required" in result.stderr.lower() or "bucket" in result.stderr.lower())

def test_s3_pit_restore_invalid_arg_public():
    """Invalid arg (e.g., --notarealarg) produces exit code 2 and usage message in stderr."""
    result = subprocess.run(
        [sys.executable, "s3-pit-restore", "--notarealarg"], capture_output=True, encoding="utf-8"
    )
    assert result.returncode == 2
    # Usage/help/error should be in stderr for invalid option
    assert ("usage" in result.stderr.lower() or "error" in result.stderr.lower())