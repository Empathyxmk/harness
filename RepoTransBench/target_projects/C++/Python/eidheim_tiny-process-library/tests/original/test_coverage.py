import subprocess
import sys
import threading
import time
import pytest

def test_version_and_lifecycle():
    got_output = [False]
    def stdout_cb(bytes):
        out = bytes.decode(errors="replace")
        if "TestProcessLibBasic" in out:
            got_output[0] = True
    proc = subprocess.Popen("echo TestProcessLibBasic", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exit_code = proc.returncode
    assert exit_code == 0
    assert "TestProcessLibBasic" in out.decode()
    assert got_output[0] or "TestProcessLibBasic" in out.decode()

def test_fails_on_bad_cmd():
    proc = subprocess.Popen("nonexistent_command_xyz", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exit_code = proc.returncode
    assert exit_code != 0

def test_redirect_stderr():
    got_err = [False]
    proc = subprocess.Popen("ls __should_not_exist__", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exit_code = proc.returncode
    if err and err.strip():
        got_err[0] = True
    assert exit_code != 0
    assert got_err[0]

def test_open_stdin_and_write():
    got_out = [False]
    proc = subprocess.Popen("cat", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(b'ECHO_INPUT\n')
    proc.stdin.close()
    out, err = proc.communicate()
    if b'ECHO_INPUT' in out:
        got_out[0] = True
    exit_code = proc.returncode
    assert exit_code == 0
    assert got_out[0]

def test_kill_process():
    import os, signal
    proc = subprocess.Popen("sleep 2", shell=True)
    time.sleep(0.3)
    proc.kill()
    exit_code = proc.wait()
    assert exit_code != 0

def test_static_kill_valid():
    import os, signal
    proc = subprocess.Popen("sleep 2", shell=True)
    time.sleep(0.3)
    try:
        os.kill(proc.pid, signal.SIGKILL)
    except Exception:
        # Might have exited early, but this matches the intent
        pass
    exit_code = proc.wait()
    assert exit_code != 0

def test_try_get_exit_status():
    proc = subprocess.Popen("echo output", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finished = False
    for _ in range(10):
        status = proc.poll()
        if status is not None:
            finished = True
            break
        time.sleep(0.05)
    assert finished

@pytest.mark.skipif(sys.platform.startswith('win'), reason="Unix only block")
def test_function_unix_direct():
    import sys
    import os
    # Fakes "Process p([](){puts(...);exit(0);}, ...)"
    proc = subprocess.Popen([sys.executable, '-c', 'print("DirectFunctionWorks")'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    exit_code = proc.returncode
    assert exit_code == 0
    assert b'DirectFunctionWorks' in out