import subprocess

def test_open_close_echo_sleep():
    result = []
    proc = subprocess.Popen("echo 'hello_public'", shell=True, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    result = out.decode()
    assert "hello_public" in result

def test_close_stdin_immediately():
    proc = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.close()
    out, err = proc.communicate()
    assert out.decode() == ""