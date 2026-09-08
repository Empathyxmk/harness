import os
import sys
import shutil
import io
import time
import builtins
import types

import pytest

_config_xml = 'config.xml'

ORIG_CONFIG = '<widget><access origin="*" /><access origin="something.com" /></widget>'
REMOVED_CONFIG = '<widget><access origin="something.com" /></widget>'

def remove_access_star(config_path=_config_xml):
    # Simulate the remove-access.js node script. Remove <access origin="*" /> from config.xml
    try:
        with open(config_path, 'r', encoding='utf8') as f:
            data = f.read()
    except Exception as e:
        print("Error reading config.xml:", str(e))
        return

    new_data = data.replace('<access origin="*" />', '')
    try:
        with open(config_path, 'w', encoding='utf8') as f:
            f.write(new_data)
        print('<access origin="*" /> removed from config.xml')
    except Exception as e:
        print("Error writing config.xml:", str(e))

@pytest.fixture(autouse=True)
def cleanup_and_restore():
    # Clean up the config.xml file before and after each test
    if os.path.exists(_config_xml):
        os.remove(_config_xml)
    yield
    if os.path.exists(_config_xml):
        os.remove(_config_xml)

def test_removes_access_star_from_config_xml(monkeypatch, capsys):
    # Write original config file
    with open(_config_xml, 'w', encoding='utf8') as f:
        f.write(ORIG_CONFIG)

    # Patch print to capture log
    remove_access_star(_config_xml)
    # Give time for async in JS, but unnecessary in Python

    with open(_config_xml, 'r', encoding='utf8') as f:
        result = f.read()
    captured = capsys.readouterr()
    assert result == REMOVED_CONFIG
    assert '<access origin="*" /> removed from config.xml' in captured.out

def test_logs_error_if_readfile_fails(monkeypatch, capsys):
    # Remove file so read fails
    if os.path.exists(_config_xml):
        os.remove(_config_xml)
    remove_access_star(_config_xml)
    captured = capsys.readouterr()
    assert "Error reading config.xml:" in captured.out

def test_logs_error_if_writefile_fails(monkeypatch, capsys):
    # Write file so we can open it for reading
    with open(_config_xml, 'w', encoding='utf8') as f:
        f.write(ORIG_CONFIG)

    def bad_write(*args, **kwargs):
        raise Exception('Simulated write error')
    # Patch builtins.open to throw when writing
    orig_open = builtins.open
    def open_patch(file, mode='r', *args, **kwargs):
        if file == _config_xml and 'w' in mode:
            raise Exception('Simulated write error')
        return orig_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, 'open', open_patch)
    remove_access_star(_config_xml)
    captured = capsys.readouterr()
    assert "Error writing config.xml:" in captured.out and "Simulated write error" in captured.out
    # Restore
    monkeypatch.setattr(builtins, 'open', orig_open)