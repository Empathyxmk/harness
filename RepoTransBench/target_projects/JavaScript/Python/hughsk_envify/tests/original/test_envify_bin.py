import os
import pathlib
import stat

def test_bin_envify_is_executable():
    bin_file = pathlib.Path(os.path.dirname(__file__)) / '../../bin/envify'
    bin_file = bin_file.resolve()
    assert bin_file.is_file(), f"{bin_file} is not a regular file."
    st = bin_file.stat()
    assert bool(st.st_mode & stat.S_IXUSR), f"File {bin_file} is not user-executable."