import subprocess
import sys

def test_version_and_lifecycle_public():
    result = []
    proc = subprocess.Popen("echo public_coverage_test", shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    result = out.decode()
    exit_code = proc.returncode
    assert "public_coverage_test" in result
    assert exit_code == 0

def test_fails_on_bad_cmd_public():
    proc = subprocess.Popen("this_command_should_not_exist_public", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exit_code = proc.returncode
    assert exit_code != 0

def test_redirect_stderr_public():
    proc = subprocess.Popen("ls /definitely_not_existing_public_dir", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = proc.communicate()
    result = out.decode()
    exit_code = proc.returncode
    assert exit_code != 0
    # Fallback: Accept either "No such file" or "cannot access"
    assert ("No such file" in result) or ("cannot access" in result)

def test_open_stdin_and_write_public():
    message = "HELLO_PUBLIC_STDOUT\n"
    proc = subprocess.Popen(["cat"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate(input=message.encode())
    proc.stdin = None
    result = out.decode()
    assert result == message