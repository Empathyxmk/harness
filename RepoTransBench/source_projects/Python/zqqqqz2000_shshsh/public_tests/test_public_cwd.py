from shshsh.global_vars import CWD
import os

def test_public_cwd():
    # The cwd should match os.getcwd()
    assert CWD == os.getcwd()