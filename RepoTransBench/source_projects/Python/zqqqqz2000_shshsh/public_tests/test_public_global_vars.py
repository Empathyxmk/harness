from shshsh.global_vars import ENV
import os

def test_public_env_vars():
    assert isinstance(ENV, dict)
    assert all(isinstance(k, str) for k in ENV)
    assert set(os.environ.items()).issubset(set(ENV.items()))