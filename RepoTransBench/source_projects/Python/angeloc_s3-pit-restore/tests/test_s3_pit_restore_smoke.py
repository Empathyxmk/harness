import subprocess
import sys

def test_s3_pit_restore_help():
    """Check --help output and exit code"""
    result = subprocess.run(
        [sys.executable, "s3-pit-restore", "--help"], capture_output=True, encoding="utf-8"
    )
    assert "usage" in result.stdout.lower()
    assert result.returncode == 0

def test_s3_pit_restore_missing_bucket():
    """If -b/--bucket missing, exit code is 2 and show error."""
    result = subprocess.run(
        [sys.executable, "s3-pit-restore", "--version"], capture_output=True, encoding="utf-8"
    )
    assert result.returncode == 2
    # Should mention missing argument
    assert ("required" in result.stderr.lower() or "bucket" in result.stderr.lower())