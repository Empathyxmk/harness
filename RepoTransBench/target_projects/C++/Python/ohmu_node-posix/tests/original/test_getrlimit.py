import pytest
import sys

def test_getrlimit(monkeypatch):
    # Most of this logic is just the shape; real implementation
    # would require binding to getrlimit/setrlimit
    limits = ["core", "cpu", "data", "fsize", "nofile", "stack", "as"]
    unsupported_limits = []

    if sys.platform in ['linux', 'darwin', 'freebsd']:
        limits.append("nproc")
    else:
        unsupported_limits.append("nproc")

    posix = pytest.importorskip("posix_py")

    # Invalid args
    with pytest.raises(Exception):
        posix.getrlimit("foobar")
    with pytest.raises(Exception):
        posix.getrlimit()
    with pytest.raises(Exception):
        posix.getrlimit(0)

    # Supported resources (the binding would need to provide getrlimit)
    for limit in limits:
        limit_val = posix.getrlimit(limit)
        print("getrlimit", limit, ":", limit_val)
        assert isinstance(limit_val['soft'], (int, type(None)))
        assert isinstance(limit_val['hard'], (int, type(None)))

    for limit in unsupported_limits:
        with pytest.raises(Exception):
            posix.getrlimit(limit)