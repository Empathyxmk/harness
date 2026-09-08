import os
import shshsh.global_vars

def test_cwd_env_exist():
    # CWD should be current working directory
    assert shshsh.global_vars.CWD == os.getcwd()
    # ENV should be a dict of environment
    assert isinstance(shshsh.global_vars.ENV, dict)
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in shshsh.global_vars.ENV.items())