from shshsh.quick import qrun

def test_public_qrun_manual():
    out = qrun("echo", "manual_test_case")
    assert b"manual_test_case" in out.stdout.read()