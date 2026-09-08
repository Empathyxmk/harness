import subprocess
import os

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result

def test_trim_paired_failures(monkeypatch):
    # With output as gzip (simulate success)
    result = run_command("python src/main.py pe -f test/test.f.fastq -r test/test.r.fastq -t sanger -o o1.fastq -p o2.fastq -s s1.fastq -g")
    assert result.returncode == 0

    # With no-fiveprime and quiet (simulate success)
    result = run_command("python src/main.py pe -f test/test.f.fastq -r test/test.r.fastq -t sanger -o o1.fastq -p o2.fastq -s s1.fastq -x --quiet")
    assert result.returncode == 0

    # Clean up files
    for fn in ["o1.fastq", "o2.fastq", "s1.fastq", "o1.fastq.gz", "o2.fastq.gz", "s1.fastq.gz"]:
        if os.path.exists(fn):
            os.remove(fn)