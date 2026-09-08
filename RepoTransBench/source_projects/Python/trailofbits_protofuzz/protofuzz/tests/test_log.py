from protofuzz import log

def test_log_debug_and_setlevel(capsys):
    log.set_level_debug(True)
    log.debug("test debug msg")
    out, err = capsys.readouterr()
    assert "test debug msg" in out or "test debug msg" in err

def test_log_disable_debug(capsys):
    log.set_level_debug(False)
    log.debug("noapi")
    out, err = capsys.readouterr()
    assert "noapi" not in out and "noapi" not in err