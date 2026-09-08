import subprocess
import os

def test_if_env_variable_matches():
    os.environ['FOO'] = 'bar'
    result = subprocess.run(['node', 'bin/if-env.js', 'FOO=bar'], capture_output=True, text=True)
    assert result.returncode == 0

def test_if_env_variable_does_not_match():
    os.environ['FOO'] = 'baz'
    result = subprocess.run(['node', 'bin/if-env.js', 'FOO=bar'], capture_output=True, text=True)
    assert result.returncode != 0

def test_if_env_multiple_variables_all_match():
    os.environ['FOO'] = 'bar'
    os.environ['BAR'] = 'baz'
    result = subprocess.run(['node', 'bin/if-env.js', 'FOO=bar', 'BAR=baz'], capture_output=True, text=True)
    assert result.returncode == 0

def test_if_env_multiple_variables_one_mismatch():
    os.environ['FOO'] = 'bar'
    os.environ['BAR'] = 'fail'
    result = subprocess.run(['node', 'bin/if-env.js', 'FOO=bar', 'BAR=baz'], capture_output=True, text=True)
    assert result.returncode != 0

def test_if_env_missing_variable():
    # Remove BAR if set
    if 'BAR' in os.environ:
        del os.environ['BAR']
    os.environ['FOO'] = 'bar'
    result = subprocess.run(['node', 'bin/if-env.js', 'FOO=bar', 'BAR=baz'], capture_output=True, text=True)
    assert result.returncode != 0