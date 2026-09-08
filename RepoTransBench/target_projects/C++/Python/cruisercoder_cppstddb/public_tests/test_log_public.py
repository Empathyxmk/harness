from cppstddb import log

def test_log_public():
    from io import StringIO
    oss = StringIO()
    log(oss, "Public test log entry %d", 55)
    msg = oss.getvalue()
    assert "Public test log entry" in msg and "55" in msg