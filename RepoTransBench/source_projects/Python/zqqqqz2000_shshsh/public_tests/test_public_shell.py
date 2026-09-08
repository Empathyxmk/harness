from shshsh import Sh

def test_public_shell_echo():
    res = Sh("echo helloworld")
    assert res.stdout.read() == b"helloworld\n"