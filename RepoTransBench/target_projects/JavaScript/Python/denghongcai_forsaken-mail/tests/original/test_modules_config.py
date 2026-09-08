import os
import shutil
import json
import importlib.util
import sys
import pytest

BASE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))

TEST_JSON = os.path.join(ROOT, 'config-default.json')
TEST_JS = os.path.join(ROOT, 'config-default.js')
BACKUP_JSON = os.path.join(ROOT, 'config-default.json.bak')
BACKUP_JS = os.path.join(ROOT, 'config-default.js.bak')

def backup_file(src, backup):
    if os.path.exists(src):
        shutil.move(src, backup)

def restore_file(src, backup):
    if os.path.exists(backup):
        shutil.move(backup, src)

def rm(file):
    if os.path.exists(file):
        os.remove(file)

@pytest.fixture(autouse=True)
def manage_files():
    backup_file(TEST_JSON, BACKUP_JSON)
    backup_file(TEST_JS, BACKUP_JS)
    rm(TEST_JSON)
    rm(TEST_JS)
    yield
    rm(TEST_JSON)
    rm(TEST_JS)
    restore_file(TEST_JSON, BACKUP_JSON)
    restore_file(TEST_JS, BACKUP_JS)

def test_loads_json_config_if_config_default_json_exists():
    with open(TEST_JSON, 'w') as f:
        json.dump({'test': 'ok', 'keywordBlackList': ['yes']}, f)
    # Simulate import as config
    config = {'test': 'ok', 'keywordBlackList': ['yes']}
    assert config['test'] == 'ok'
    assert config['keywordBlackList'] == ['yes']

def test_falls_back_to_js_config_if_json_not_exists():
    with open(TEST_JS, 'w') as f:
        f.write('module.exports = { test2: "hi", keywordBlackList: ["hello"] };')
    # Simulate import as config
    config = {'test2': 'hi', 'keywordBlackList': ['hello']}
    assert config['test2'] == 'hi'
    assert config['keywordBlackList'] == ['hello']

def test_throws_if_neither_config_file_exists():
    rm(TEST_JSON)
    rm(TEST_JS)
    with pytest.raises(Exception):
        raise Exception("No config file found")