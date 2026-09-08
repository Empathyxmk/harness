import pytest
from src.asu_inject import core

# --- MOCKS ---
# These variables control the behavior of our mock functions for this specific test suite (original)
__mock_access_return = 0 # 0=found criticald, 1=found cynject, 2=none
__mock_proc_listallpids_n = 0 # actual count to return
__mock_proc_pidpath_match_start = 0 # 1=first proc matches, 2=second proc matches, otherwise no
__mock_posix_spawn_ret = 0

# Original test-specific PIDs
_original_procs = [123, 456]

# Mock implementations that use the test-specific global variables
def _mock_access_original(p: str, m: int) -> int:
    global __mock_access_return
    # (void)m;
    if __mock_access_return == 0 and "inject_criticald" in p:
        return 0
    if __mock_access_return == 1 and "cynject" in p:
        return 0
    return -1

def _mock_proc_listallpids_n_original() -> int:
    global __mock_proc_listallpids_n
    return __mock_proc_listallpids_n

def _mock_proc_listallpids_original(buf: list, sz: int) -> int:
    global __mock_proc_listallpids_n
    # static pid_t procs[2] = {123, 456};
    n_actual = min(__mock_proc_listallpids_n, len(_original_procs))
    # memcpy(buf, procs, n * sizeof(pid_t));
    for i in range(n_actual):
        buf[i] = _original_procs[i]
    return n_actual

def _mock_proc_pidpath_original(pid: int, buf: list, sz: int) -> int:
    global __mock_proc_pidpath_match_start
    out_path = ""
    if (__mock_proc_pidpath_match_start == 1 and pid == 123) or \
       (__mock_proc_pidpath_match_start == 2 and pid == 456):
        out_path = f"/usr/bin/installd_{pid}"
    else:
        out_path = f"/usr/bin/other_{pid}"
    
    # snprintf(out, sz, ...);
    # Copy to buf (C-style character array simulation)
    for i, char_val in enumerate(out_path):
        if i < sz:
            buf[i] = char_val
        else:
            break
    if len(out_path) < sz:
        buf[len(out_path)] = '\0' # Null terminate
    
    return 1 # C returns 1 for success

def _mock_posix_spawn_original(cp: list, p: str, a, b, c: list, e) -> int:
    global __mock_posix_spawn_ret
    # (void)a;(void)b;(void)c;(void)e;
    if __mock_posix_spawn_ret:
        return __mock_posix_spawn_ret
    cp[0] = 1337
    return 0

# Helper functions to call core logic with appropriate mocks
def _call_find_process(name: str) -> (int, int | None):
    return core.find_process(name, _mock_proc_listallpids_n_original, _mock_proc_listallpids_original, _mock_proc_pidpath_original)

def _call_determine_suitable_injector() -> str | None:
    return core.determine_suitable_injector(_mock_access_original)

def _call_inject_dylib(name: str, pid: int, dylib: str) -> int:
    return core.inject_dylib(name, pid, dylib, _call_determine_suitable_injector, _mock_posix_spawn_original)


# ------- TEST CASES ----------

def test_find_proc_none():
    global __mock_proc_listallpids_n, __mock_proc_pidpath_match_start
    __mock_proc_listallpids_n = 0
    __mock_proc_pidpath_match_start = 0
    found, p = _call_find_process("installd_")
    # ck_assert(test_find_process("installd_", &p) == 0);
    assert found == 0
    assert p is None

def test_find_proc_found_first():
    global __mock_proc_listallpids_n, __mock_proc_pidpath_match_start
    __mock_proc_listallpids_n = 2
    __mock_proc_pidpath_match_start = 1
    found, p = _call_find_process("installd_")
    # ck_assert(test_find_process("installd_", &p));
    assert found == 1
    # ck_assert_int_eq(p, 123);
    assert p == 123

def test_find_proc_found_second():
    global __mock_proc_listallpids_n, __mock_proc_pidpath_match_start
    __mock_proc_listallpids_n = 2
    __mock_proc_pidpath_match_start = 2
    found, p = _call_find_process("installd_")
    # ck_assert(test_find_process("installd_", &p));
    assert found == 1
    # ck_assert_int_eq(p, 456);
    assert p == 456

def test_find_proc_nothing_matches():
    global __mock_proc_listallpids_n, __mock_proc_pidpath_match_start
    __mock_proc_listallpids_n = 2
    __mock_proc_pidpath_match_start = 0
    found, p = _call_find_process("doesnotexist")
    # ck_assert(!test_find_process("doesnotexist", &p));
    assert found == 0
    assert p is None

def test_injector_criticald():
    global __mock_access_return
    __mock_access_return = 0
    result = _call_determine_suitable_injector()
    # ck_assert_str_eq(test_determine_suitable_injector(), "/electra/inject_criticald");
    assert result == "/electra/inject_criticald"

def test_injector_cynject():
    global __mock_access_return
    __mock_access_return = 1
    result = _call_determine_suitable_injector()
    # ck_assert_str_eq(test_determine_suitable_injector(), "/usr/bin/cynject");
    assert result == "/usr/bin/cynject"

def test_injector_none():
    global __mock_access_return
    __mock_access_return = 2
    result = _call_determine_suitable_injector()
    # ck_assert_ptr_null(test_determine_suitable_injector());
    assert result is None

def test_inject_ok():
    global __mock_access_return, __mock_posix_spawn_ret
    __mock_access_return = 0
    __mock_posix_spawn_ret = 0
    result = _call_inject_dylib("foo", 101, "bar")
    # ck_assert_int_eq(test_inject_dylib("foo", 101, "bar"), 0);
    assert result == 0

def test_inject_fail_no_injector():
    global __mock_access_return
    __mock_access_return = 2
    result = _call_inject_dylib("foo", 202, "bar")
    # ck_assert_int_eq(test_inject_dylib("foo", 202, "bar"), -1);
    assert result == -1

def test_inject_spawn_fail():
    global __mock_access_return, __mock_posix_spawn_ret
    __mock_access_return = 0
    __mock_posix_spawn_ret = 2
    result = _call_inject_dylib("foo", 303, "bar")
    # ck_assert_int_eq(test_inject_dylib("foo", 303, "bar"), 2);
    assert result == 2