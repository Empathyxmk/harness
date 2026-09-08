from tests.original.debug_helper import debug

def test_debug_message(capsys):
    debug("This is a test message.")
    out = capsys.readouterr().out
    assert "This is a test message." in out