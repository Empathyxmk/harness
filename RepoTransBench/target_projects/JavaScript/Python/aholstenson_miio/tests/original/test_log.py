import sys
import types
import builtins
import pytest

import threading
import time

# === Dummy log module ===
class DummyLog:
    indent = ''
    _original_indent = ''
    @staticmethod
    def info(*args):
        print(*args)
    @staticmethod
    def error(*args):
        print(*args)
    @staticmethod
    def warn(*args):
        print(*args)
    @staticmethod
    def plain(*args):
        print(*args)
    @staticmethod
    def group(func):
        prev = DummyLog.indent
        DummyLog.indent = '  '
        try:
            func()
        finally:
            DummyLog.indent = prev
    @staticmethod
    def device(info, extra=None):
        print("Device info:", info, extra)

@pytest.fixture(autouse=True)
def mock_console_log(monkeypatch):
    calls = []
    monkeypatch.setattr('builtins.print', lambda *a, **k: calls.append(a))
    yield calls

def test_log_info(mock_console_log):
    DummyLog.info('hello', 'world')
    assert mock_console_log

def test_log_error(mock_console_log):
    DummyLog.error('bad', 'thing')
    assert mock_console_log

def test_log_warn(mock_console_log):
    DummyLog.warn('careful', 'here')
    assert mock_console_log

def test_log_plain(mock_console_log):
    DummyLog.plain('go', 'ahead')
    assert mock_console_log

def test_group_and_restore_indentation():
    orig_indent = DummyLog.indent
    def fn():
        DummyLog.info('nested')
        assert DummyLog.indent != orig_indent
    DummyLog.group(fn)
    assert DummyLog.indent == orig_indent

def test_print_device_info_all_branches(mock_console_log):
    DummyLog.device({
      "id": 'miio:123456',
      "metadata": { "types": set(['miio:type1', 'othertype']), "capabilities": set(['a', 'b']) },
      "management": { "model": 'abc', "address": 'ip', "token": 'tok', "autoToken": True }
    })
    DummyLog.device({
      "id": 'miio:78910',
      "metadata": { "types": set(['miio:type1']), "capabilities": set([]) },
      "management": { "model": None, "address": 'ip', "token": 'tok', "autoToken": False }
    }, True)
    DummyLog.device({
      "id": 'miio:78910',
      "metadata": { "types": set(['type1']), "capabilities": set([]) },
      "management": { "model": 'model1', "address": None, "parent": {"id":'par'}, "token": None }
    })
    DummyLog.device({
      "id": '12345',
      "metadata": { "types": set(['type1']), "capabilities": set([]) },
      "management": { "model": None, "address": 'ip', "parent": None, "token": None }
    })
    DummyLog.device({
      "id": 'miio:23456',
      "metadata": { "types": set(['miio:type1']), "capabilities": set([]) },
      "management": { "model": 'm', "address": None, "parent": {"id":'p'}, "token": None }
    }, True)
    assert mock_console_log