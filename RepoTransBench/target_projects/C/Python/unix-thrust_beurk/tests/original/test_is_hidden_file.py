import pytest

MAGIC_STRING = "MAGIC"
LIBRARY_NAME = "libbeurk.so"
PROC_PATH = "/proc/"
_STAT_VER = 0
MAX_LEN = 128
ENV_LINE = "%s/environ"
HIDDEN_ENV_VAR = "BEURK_ATK_ENV"

stat_success = 0
envfile_open = 0

dummy_env_lines_to_return = []
dummy_env_idx = 0

def set_dummy_env_content(lines):
    global dummy_env_lines_to_return, dummy_env_idx
    dummy_env_lines_to_return = list(lines)
    dummy_env_idx = 0

# Simulate stat
def REAL___XSTAT(ver, path, s_fstat):
    global stat_success
    return 0 if stat_success else -1

# Simulate file open for environ
def REAL_FOPEN(path, mode):
    global envfile_open
    if envfile_open:
        return 'dummy_env_file'
    return None

def fgets_mock(f):
    global dummy_env_idx, dummy_env_lines_to_return
    if f == 'dummy_env_file' and dummy_env_idx < len(dummy_env_lines_to_return):
        s = dummy_env_lines_to_return[dummy_env_idx]
        dummy_env_idx += 1
        return s
    return None

def fclose_mock(f):
    # No-op
    pass

def check_env(haystack, needle):
    return needle in haystack

def is_hidden_file(path):
    global stat_success, envfile_open
    def memset(line):
        # just resetting to ''
        return ""

    # Simulate C's: if (strstr(path, MAGIC_STRING) || strstr(path, LIBRARY_NAME))
    if MAGIC_STRING in path or LIBRARY_NAME in path:
        return 1

    # Simulate C's: if (strstr(path, PROC_PATH))...
    if PROC_PATH in path:
        s_fstat = None
        if REAL___XSTAT(_STAT_VER, path, s_fstat) != -1:
            environ = ENV_LINE % path
            if REAL___XSTAT(_STAT_VER, environ, s_fstat) != -1:
                env_file = REAL_FOPEN(environ, 'r')
                if env_file:
                    while True:
                        line = fgets_mock(env_file)
                        if line is None:
                            break
                        if check_env(line, HIDDEN_ENV_VAR):
                            fclose_mock(env_file)
                            return 1
                        # memset(line, 0x00, MAX_LEN) - simulated by line assignment
                    fclose_mock(env_file)
    return 0

def test_hidden_by_magic():
    assert is_hidden_file("/tmp/MAGIC.txt") == 1

def test_hidden_by_libraryname():
    assert is_hidden_file("/libbeurk.so") == 1

def test_hidden_by_proc_path_found():
    global stat_success, envfile_open
    stat_success = 1
    envfile_open = 1
    set_dummy_env_content(["BEURK_ATK_ENV=1"])
    assert is_hidden_file("/proc/1234") == 1
    envfile_open = 0
    stat_success = 0

def test_not_hidden_non_proc():
    assert is_hidden_file("/etc/shadow") == 0

def test_not_hidden_proc_env_missing():
    global stat_success, envfile_open
    stat_success = 0
    envfile_open = 0
    assert is_hidden_file("/proc/999") == 0

def test_not_hidden_proc_env_found_but_not_atk():
    global stat_success, envfile_open
    stat_success = 1
    envfile_open = 1
    set_dummy_env_content(["NORMAL_ENV=1"])
    assert is_hidden_file("/proc/1234") == 0
    envfile_open = 0
    stat_success = 0

def test_not_hidden_proc_envfile_null():
    global stat_success, envfile_open
    stat_success = 1
    envfile_open = 0
    assert is_hidden_file("/proc/5432") == 0
    envfile_open = 0
    stat_success = 0

def test_proc_envfile_nolines():
    global stat_success, envfile_open
    stat_success = 1
    envfile_open = 1
    set_dummy_env_content([])
    assert is_hidden_file("/proc/4321") == 0
    envfile_open = 0
    stat_success = 0

def test_proc_envfile_multiple_lines_with_atk():
    global stat_success, envfile_open
    stat_success = 1
    envfile_open = 1
    set_dummy_env_content(["NORMAL_ENV=1", "BEURK_ATK_ENV=1"])
    assert is_hidden_file("/proc/4242") == 1
    envfile_open = 0
    stat_success = 0

def test_proc_envfile_multiple_lines_no_atk():
    global stat_success, envfile_open
    stat_success = 1
    envfile_open = 1
    set_dummy_env_content(["NORMAL_ENV=1", "USER_ENV=2"])
    assert is_hidden_file("/proc/5252") == 0
    envfile_open = 0
    stat_success = 0