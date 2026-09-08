import subprocess
import os

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result

def test_trim_paired_args(monkeypatch):
    # Missing required args
    result = run_command("python src/main.py pe")
    assert result.returncode != 0

    # Single input should fail (missing pair)
    result = run_command("python src/main.py pe -f test/test.f.fastq -t sanger -o out1.fastq -p out2.fastq -s single.fastq")
    assert result.returncode != 0

    # All required args should succeed
    result = run_command("python src/main.py pe -f test/test.f.fastq -r test/test.r.fastq -t sanger -o out1.fastq -p out2.fastq -s single.fastq")
    assert result.returncode == 0

    # Clean up
    for fn in ("out1.fastq", "out2.fastq", "single.fastq"):
        if os.path.exists(fn):
            os.remove(fn)