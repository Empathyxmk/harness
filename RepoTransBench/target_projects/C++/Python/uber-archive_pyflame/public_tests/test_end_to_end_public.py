import os
import subprocess
import sys
import tempfile
import time
import pytest
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_pyflame(args, timeout=8, capture_output=True, **kwargs):
    pyflame_bin = shutil.which('pyflame') or os.path.join(os.path.dirname(SCRIPT_DIR), 'src', 'pyflame')
    if not os.path.exists(pyflame_bin):
        raise RuntimeError(f"pyflame not found: {pyflame_bin}")
    cmd = [pyflame_bin] + args
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        **kwargs
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise
    return proc.returncode, stdout, stderr

@pytest.fixture
def sleeper_script_path(tmp_path):
    script = os.path.join(SCRIPT_DIR, "threaded_sleeper.py")
    assert os.path.exists(script)
    return script

@pytest.fixture
def alt_python_program(tmp_path):
    script = os.path.join(SCRIPT_DIR, "forker.py")
    assert os.path.exists(script)
    return script

def test_pyflame_trace_on_threaded_sleeper(sleeper_script_path):
    python_bin = sys.executable
    proc = subprocess.Popen([python_bin, sleeper_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.75)
    try:
        rc, out, err = run_pyflame(["-p", str(proc.pid)], timeout=10)
        assert rc == 0
        assert b"threaded_sleeper" in out
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()

def test_pyflame_on_forker_script(alt_python_program):
    python_bin = sys.executable
    proc = subprocess.Popen([python_bin, alt_python_program], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.50)
    try:
        rc, out, err = run_pyflame(["-p", str(proc.pid)], timeout=10)
        assert rc == 0
        assert b"forker" in out or b"child" in out or b"parent" in out
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()

def test_pyflame_with_env(monkeypatch, sleeper_script_path):
    python_bin = sys.executable
    monkeypatch.setenv("MY_PUBLIC_TEST_VAR", "Zebra")
    proc = subprocess.Popen([python_bin, sleeper_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(0.75)
    try:
        rc, out, err = run_pyflame(["-p", str(proc.pid)], timeout=10)
        assert rc == 0
        assert b"threaded_sleeper" in out
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()