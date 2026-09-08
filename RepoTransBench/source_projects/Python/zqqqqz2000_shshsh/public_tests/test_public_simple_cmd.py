from shshsh import Sh

def test_public_simple_echo():
    res = Sh("echo PUBTEST_123")
    assert res.stdout.read() == b"PUBTEST_123\n"