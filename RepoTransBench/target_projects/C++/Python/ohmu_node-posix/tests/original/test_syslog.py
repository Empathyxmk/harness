import pytest

def test_syslog_errors():
    posix = pytest.importorskip("posix_py")
    with pytest.raises(Exception):
        posix.openlog("foobar", 1)
    with pytest.raises(Exception):
        posix.closelog("foobar")
    with pytest.raises(Exception):
        posix.openlog("foobar", {"xxx": 1}, "local0")
    with pytest.raises(Exception):
        posix.openlog("foobar", {}, "xxx")
    posix.openlog("test-node-syslog", {"cons": True, "ndelay": True, "pid": True}, "local0")
    posix.setlogmask({"info": 1, "debug": 1})
    old = posix.setlogmask({"emerg": 1, "alert": 1, "crit": 1, "err": 1,
                            "warning": 1, "notice": 1, "info": 1, "debug": 1})
    posix.syslog("info", "hello from node-posix (info)")
    posix.closelog()