import subprocess

def test_open_close_echo():
    for c in range(10000):
        cmd = f"echo Hello World {c}"
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        decoded = out.decode(errors="replace")
        expected = f"Hello World {c}\n"
        if decoded != expected:
            print(f"Wrong output to stdout. Got '{decoded}', expected '{expected}'")
            assert False
        if proc.returncode != 0:
            print("Process returned failure.")
            assert False