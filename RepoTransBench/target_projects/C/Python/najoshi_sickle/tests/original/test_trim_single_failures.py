import subprocess
import os

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result

def test_trim_single_failures(monkeypatch):
    # With truncated N
    with open('test/tmp_n.fastq', 'w') as f:
        f.write("@seq1\nACGNTAAA\n+\nIIIIIIII\n")
    result = run_command("python src/main.py se -f test/tmp_n.fastq -t sanger -o out.fastq -n")
    assert result.returncode == 0

    # Quiet option
    result = run_command("python src/main.py se -f test/test.fastq -t sanger -o out.fastq --quiet")
    assert result.returncode == 0

    # No-fiveprime flag
    result = run_command("python src/main.py se -f test/test.fastq -t sanger -o out.fastq -x")
    assert result.returncode == 0

    # Clean up
    os.remove("out.fastq")
    os.remove("test/tmp_n.fastq")