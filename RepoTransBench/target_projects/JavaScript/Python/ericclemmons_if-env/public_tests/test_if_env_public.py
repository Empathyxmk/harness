import subprocess
import os

def test_if_env_public_single_var_match():
    os.environ['HELLO'] = 'WORLD'
    result = subprocess.run(['node', 'bin/if-env.js', 'HELLO=WORLD'], capture_output=True, text=True)
    assert result.returncode == 0

def test_if_env_public_single_var_no_match():
    os.environ['HELLO'] = 'THERE'
    result = subprocess.run(['node', 'bin/if-env.js', 'HELLO=WORLD'], capture_output=True, text=True)
    assert result.returncode != 0

def test_if_env_public_var_not_set():
    if 'HELLO' in os.environ:
        del os.environ['HELLO']
    result = subprocess.run(['node', 'bin/if-env.js', 'HELLO=WORLD'], capture_output=True, text=True)
    assert result.returncode != 0