from tests.original.debug_helper import debug

def test_public_debug(capsys):
    debug("Testing public debug...")
    out = capsys.readouterr().out
    assert "public debug" in out