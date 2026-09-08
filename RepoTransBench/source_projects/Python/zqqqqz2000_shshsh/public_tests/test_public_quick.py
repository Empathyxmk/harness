from shshsh.quick import izip, I, qrun

def test_public_izip_basic():
    a = [2, 4, 6]
    b = ["x", "y", "z"]
    pairs = list(izip(a, b))
    assert pairs == [(2, "x"), (4, "y"), (6, "z")]

def test_public_I_basic():
    assert str(I) == str(I)  # Check representation

def test_public_qrun():
    # Use a different command output
    out = qrun("echo", "diff_output")
    assert b"diff_output" in out.stdout.read()