import sparts.daemon as daemon

def test_get_pid_none(monkeypatch):
    # Should return None if /var/run/XXX.pid does not exist
    monkeypatch.setattr(daemon.os.path, "isfile", lambda f: False)
    assert daemon.get_pid("/var/run/xxx") is None

def test_daemonize_nofork(monkeypatch):
    # Should not fork if 'nofork' is True, should just call target()
    called = {}
    def target(): called['ran'] = True
    daemon.daemonize(target, nofork=True)
    assert called.get('ran', False) is True

def test_daemonize_pidfile(tmp_path):
    # Touch a PID file, ensure that on process re-run it is removed
    pidfile = tmp_path / "foo.pid"
    pidfile.write_text("1234")
    removed = {}
    def target(): pass
    def remove(path): removed['called'] = True
    import os
    os_remove = daemon.os.remove
    daemon.os.remove = remove
    try:
        daemon.daemonize(target, pidfile=str(pidfile), nofork=True)
        assert removed.get('called', False)
    finally:
        daemon.os.remove = os_remove