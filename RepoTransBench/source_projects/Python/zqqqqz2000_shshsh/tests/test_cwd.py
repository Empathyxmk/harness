import os
import tempfile
from shshsh import utils

def test_ch_cwd():
    orig_dir = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        with utils.cwd(tmp):
            assert os.getcwd() == tmp
        assert os.getcwd() == orig_dir