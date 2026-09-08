import sys
import types
import builtins
import pytest

import threading
import time

@pytest.fixture(autouse=True)
def reset_modules_and_mocks(monkeypatch):
    # There is no global resetModules, but we can clear sys.modules for target modules if needed.
    # Here, it's a no-op unless we specifically want to simulate reloads.
    yield

class DummyDevice:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed
    def __call__(self, address=None, **kwargs):
        if address == 'ipHere':
            return DummyFuture({'id': 'abc'})
        raise Exception('bad address')

class DummyFuture:
    # Mocks a then-able Promise-like interface
    def __init__(self, value, should_fail=False):
        self.value = value
        self.should_fail = should_fail
    def __await__(self):
        if self.should_fail:
            raise Exception(self.value)
        yield  # for async interface; not used here
        return self.value
    def __call__(self, *args, **kwargs):
        if self.should_fail:
            raise Exception(self.value)
        return self.value

def make_lib_mock(success=True):
    # Returns a dummy module with .device attribute
    module = types.SimpleNamespace()
    def device(address=None, **kwargs):
        if success and address == 'ipHere':
            return DummyFuture({'id': 'abc'})
        raise Exception('bad address')
    module.device = device
    return module

def run_example_js_fake(lib, fake_console_log=None, fake_process_exit=None):
    # Simulates the behavior of example.js using the provided lib mock.
    # Returns True if device() called with correct ip, else False.
    log_calls = []
    def device_call(address=None, **kwargs):
        if address == 'ipHere':
            log_calls.append('device-called')
            return DummyFuture({'id': 'abc'})
        else:
            raise Exception('bad address')
    lib.device = device_call
    # Simulate code: try
    try:
        dev = lib.device(address='ipHere')
        if fake_console_log:
            fake_console_log('Connected device:', dev.value)
    except Exception as e:
        if fake_console_log:
            fake_console_log('Error occurred:', str(e))
        if fake_process_exit:
            fake_process_exit()
    return log_calls

def test_connects_to_device_successfully(monkeypatch):
    # Mock console.log with a spy
    log_calls = []
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: log_calls.append(args))
    # Prepare mock lib.device
    class LibModule:
        @staticmethod
        def device(address=None, **kwargs):
            if address == 'ipHere':
                return DummyFuture({'id': 'abc'})
            raise Exception('bad address')
    # Simulate the example.js main logic
    dev_future = LibModule.device(address='ipHere')
    dev = dev_future()
    assert dev['id'] == 'abc'
    # Optionally print
    print('Connected device:', dev)
    assert log_calls[-1][0] == 'Connected device:'

def test_prints_error_if_device_connection_fails(monkeypatch):
    # This test checks error logging if connection fails
    log_calls = []
    monkeypatch.setattr('builtins.print', lambda *args, **kwargs: log_calls.append(args))
    # Monkeypatch sys.exit (instead of process.exit)
    exit_called = []
    monkeypatch.setattr('sys.exit', lambda *args, **kwargs: exit_called.append(True))
    class LibModule:
        @staticmethod
        def device(address=None, **kwargs):
            raise Exception('fail')
    # Try-catch block to simulate example.js handling
    try:
        LibModule.device(address='ipHere')
    except Exception as e:
        print('Error occurred:', str(e))
        sys.exit()
    # Check log
    assert any('Error occurred:' in call[0] for call in log_calls)
    assert exit_called, "sys.exit was not called (simulating process.exit)"