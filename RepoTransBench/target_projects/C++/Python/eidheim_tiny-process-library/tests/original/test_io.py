import subprocess
import sys
import threading
import time
import pytest

def run_process(command, input_data=None, shell=True, stdout_handler=None, stderr_handler=None, open_stdin=False):
    if isinstance(command, list):
        args = command
        shell = False
    else:
        args = command
    if open_stdin or input_data is not None:
        stdin = subprocess.PIPE
    else:
        stdin = None
    proc = subprocess.Popen(
        args,
        shell=shell,
        stdin=stdin,
        stdout=subprocess.PIPE if stdout_handler is not None else None,
        stderr=subprocess.PIPE if stderr_handler is not None else None,
        universal_newlines=False
    )
    out, err = b'', b''
    if stdout_handler or stderr_handler:
        # Read in background if needed
        stdout_data, stderr_data = [], []
        def readout():
            while True:
                chunk = proc.stdout.read(1024)
                if not chunk:
                    break
                stdout_data.append(chunk)
                if stdout_handler:
                    stdout_handler(chunk)
        def readerr():
            while True:
                chunk = proc.stderr.read(1024)
                if not chunk:
                    break
                stderr_data.append(chunk)
                if stderr_handler:
                    stderr_handler(chunk)
        threads = []
        if proc.stdout:
            t = threading.Thread(target=readout)
            t.start()
            threads.append(t)
        if proc.stderr:
            t2 = threading.Thread(target=readerr)
            t2.start()
            threads.append(t2)
        if input_data is not None:
            if isinstance(input_data, str):
                input_data = input_data.encode()
            proc.stdin.write(input_data)
            proc.stdin.close()
        for t in threads:
            t.join()
        exit_code = proc.wait()
        out = b''.join(stdout_data).decode(errors="replace") if stdout_data else ''
        err = b''.join(stderr_data).decode(errors="replace") if stderr_data else ''
        return exit_code, out, err, proc
    else:
        out, err = proc.communicate(input=input_data.encode() if isinstance(input_data, str) else input_data)
        exit_code = proc.wait()
        return exit_code, out.decode(errors="replace") if out else '', err.decode(errors="replace") if err else '', proc

def test_echo_basic():
    # Simulate: Process("echo Test", ...) output handler: append output
    output = []
    exit_code, out, _, _ = run_process("echo Test", stdout_handler=lambda b: output.append(b.decode(errors="replace")))
    assert exit_code == 0
    full_output = ''.join(output)
    # Remove newline; C++ likely expects "Test" at start, not "Test\n"
    assert full_output.startswith("Test")
    output.clear()

@pytest.mark.skipif(sys.platform.startswith('win'), reason="Unix only block")
def test_echo_function_like_cpp_lambda():
    # Simulate: Process(lambda: print("Test"), ...)
    # Use python -c for inline print
    output = []
    exit_code, out, _, _ = run_process([sys.executable, '-c', 'import sys; print("Test")'], stdout_handler=lambda b: output.append(b.decode(errors="replace")))
    assert exit_code == 0
    full_output = ''.join(output)
    assert full_output.startswith("Test")
    output.clear()

def test_echo_and_ls_bad_path():
    # Simulate: echo Test && ls an_incorrect_path
    output, error = [], []
    cmd = "echo Test && ls an_incorrect_path"
    exit_code, out, err, _ = run_process(cmd, stdout_handler=lambda b: output.append(b.decode(errors="replace")), stderr_handler=lambda b: error.append(b.decode(errors="replace")))
    assert exit_code > 0
    full_output = ''.join(output)
    assert full_output.startswith("Test")
    assert any(len(e) > 0 for e in error) or len(err) > 0
    output.clear()
    error.clear()

def test_bash_echo_via_stdin():
    output = []
    proc = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(b'echo Test\n')
    proc.stdin.write(b'exit\n')
    proc.stdin.flush()
    out, err = proc.communicate()
    exit_code = proc.returncode
    result = out.decode(errors="replace")
    assert exit_code == 0
    assert "Test" in result

def test_cat_input():
    output = []
    proc = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.stdin.write(b'Test\n')
    proc.stdin.close()
    out, err = proc.communicate()
    exit_code = proc.returncode
    result = out.decode(errors="replace")
    assert exit_code == 0
    assert result.startswith("Test")

def test_try_get_exit_status_sleep():
    # Simulate: Process("sleep 5") and try_get_exit_status as in C++
    proc = subprocess.Popen('sleep 5', shell=True)
    exit_status = -2
    # There is no 'try_get_exit_status'. Instead, poll.
    assert proc.poll() is None
    assert exit_status == -2
    time.sleep(3)
    assert proc.poll() is None
    assert exit_status == -2
    time.sleep(5)
    # Should be finished now
    status = proc.poll()
    if status is None:
        proc.wait()
        status = proc.returncode
    assert status == 0