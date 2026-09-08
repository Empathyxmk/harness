import subprocess

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result

def test_sickle_args(monkeypatch):
    # No args: should fail
    result = run_command("python src/main.py")
    assert result.returncode != 0

    # Nonsense command: should fail
    result = run_command("python src/main.py nonsense")
    assert result.returncode != 0

    # --help: should show usage and succeed
    result = run_command("python src/main.py --help")
    assert result.returncode == 0
    assert b"Usage: sickle" in result.stdout

    # --version: should show version and succeed
    result = run_command("python src/main.py --version")
    assert result.returncode == 0
    assert b"sickle version" in result.stdout