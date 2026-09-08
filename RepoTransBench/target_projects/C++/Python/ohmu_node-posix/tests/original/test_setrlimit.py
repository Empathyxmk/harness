import pytest
import sys

def test_setrlimit(monkeypatch):
    # Real implementation would require os.setrlimit
    limits = ["core", "cpu", "data", "fsize", "nofile", "stack", "as"]
    unsupported_limits = []
    if sys.platform in ['linux', 'darwin', 'freebsd']:
        limits.append("nproc")
    else:
        unsupported_limits.append("nproc")

    posix = pytest.importorskip("posix_py")

    with pytest.raises(Exception):
        posix.setrlimit()
    with pytest.raises(Exception):
        posix.setrlimit("nofile")
    with pytest.raises(Exception):
        posix.setrlimit("foobar", {"soft": 100})

    # RLIM_INFINITY <-> None conversion not easily ported
    posix.setrlimit("cpu", {"soft": None, "hard": None})
    now = posix.getrlimit("cpu")
    assert now["soft"] is None
    assert now["hard"] is None

    begin = posix.getrlimit("nofile")
    print("begin:", begin)
    posix.setrlimit("nofile", {"soft": 500})
    now = posix.getrlimit("nofile")
    print("now:", now)
    assert begin["hard"] == now["hard"]
    assert now["soft"] == 500

    for lim in limits:
        limit = posix.getrlimit(lim)
        if limit["soft"] > 1:
            print("setrlimit:", lim, limit)
            posix.setrlimit(lim, {"soft": limit["soft"] - 1, "hard": limit["hard"]})
            limit2 = posix.getrlimit(lim)
            assert limit2["soft"] == limit["soft"] - 1
            print(lim, "was:", limit)
            print(lim, "now:", limit2)

    for u in unsupported_limits:
        with pytest.raises(Exception):
            posix.setrlimit(u, {"soft": 100})