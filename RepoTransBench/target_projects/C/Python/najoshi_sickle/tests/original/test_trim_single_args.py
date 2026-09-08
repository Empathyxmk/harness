import subprocess
import os
import tempfile

def run_command(cmd):
    # Simulate: call Python code that parses args and returns appropriate status
    # Should raise CalledProcessError if exit code != 0
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result

def test_trim_single_args_invalid(monkeypatch):
    # Missing required args: should return error
    result = run_command("python src/main.py se")
    assert result.returncode != 0

    # Invalid qual-type: should return error
    result = run_command("python src/main.py se -f test/test.fastq -t notqual -o out.fastq")
    assert result.returncode != 0

    # Negative quality threshold
    result = run_command("python src/main.py se -f test/test.fastq -t sanger -o out.fastq -q -1")
    assert result.returncode != 0

    # Negative length threshold
    result = run_command("python src/main.py se -f test/test.fastq -t sanger -o out.fastq -l -5")
    assert result.returncode != 0

def test_trim_single_args_happy(monkeypatch):
    # "Happy path": minimum args, should succeed (simulate OK, return 0)
    result = run_command("python src/main.py se -f test/test.fastq -t sanger -o out.fastq")
    assert result.returncode == 0
    # Clean up
    if os.path.exists("out.fastq"):
        os.remove("out.fastq")