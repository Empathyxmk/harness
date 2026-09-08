import pytest

def throws_message(cb, msg):
    with pytest.raises(Exception) as exc:
        cb()
    assert msg in str(exc.value)

def test_setpgid_errors():
    posix = pytest.importorskip("posix_py")
    throws_message(lambda: posix.setpgid(1), "setpgid: takes exactly two arguments")
    throws_message(lambda: posix.setpgid(1, 2, 3), "setpgid: takes exactly two arguments")
    throws_message(lambda: posix.setpgid("foo", 0), "setpgid: first argument must be an integer")
    throws_message(lambda: posix.setpgid(1, "bar"), "setpgid: first argument must be an integer")
    throws_message(lambda: posix.setpgid(999999, 999999), "setpgid")

def test_geteuid_getegid_errors():
    posix = pytest.importorskip("posix_py")
    throws_message(lambda: posix.geteuid(1), "geteuid: takes no arguments")
    throws_message(lambda: posix.getegid(1), "getegid: takes no arguments")

def test_setsid_errors():
    posix = pytest.importorskip("posix_py")
    throws_message(lambda: posix.setsid(1), "setsid: takes no arguments")
    try:
        posix.setsid()
    except Exception:
        pass

def test_chroot_errors():
    posix = pytest.importorskip("posix_py")
    throws_message(lambda: posix.chroot(), "chroot: takes exactly one argument")
    throws_message(lambda: posix.chroot(1), "chroot: first argument must be a string")
    throws_message(lambda: posix.chroot('/this/should/not/exist/xyz'), "chroot: chdir: ")