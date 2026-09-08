import os
import tempfile
from src.appuninstall import uninstall

def create_pid_file(filepath, pid):
    with open(filepath, "w") as f:
        f.write(f"{pid}\n")

def test_is_process_alive_self():
    # Create a pid file for self and check
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        pidfile = tf.name
    try:
        create_pid_file(pidfile, os.getpid())
        ret = uninstall.is_process_alive(pidfile)
        assert ret == 1
    finally:
        os.unlink(pidfile)

def test_is_process_alive_dead_pid():
    # Use a "dead" pid (999999 almost never exists)
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        pidfile = tf.name
    try:
        create_pid_file(pidfile, 999999)
        ret = uninstall.is_process_alive(pidfile)
        assert ret == 0
    finally:
        os.unlink(pidfile)

def test_write_pid_file_overwrite():
    # Overwrite an existing file, should update with current pid
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        pidfile = tf.name
    try:
        with open(pidfile, "w") as f:
            f.write("olddata")
        uninstall.write_pid_file(pidfile)
        with open(pidfile, "r") as f:
            data = f.readline()
        pid_from_file = int(data.strip())
        assert pid_from_file == os.getpid()
    finally:
        os.unlink(pidfile)

def test_jstring_to_cstr_env_null_but_jstr_nonnull():
    dummy = object()
    ret = uninstall.jstring_to_cstr(None, dummy)
    assert ret is None

def test_upload_stat_data_null_params():
    result = uninstall.upload_stat_data(None, -1)
    assert result == -1