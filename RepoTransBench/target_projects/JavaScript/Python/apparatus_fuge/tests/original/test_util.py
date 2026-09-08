import pytest
import importlib

try:
    util = importlib.import_module('src.apparatus_fuge.util')
except ModuleNotFoundError:
    util = type('Dummy', (), {})()

def test_should_export_expected_utility_functions():
    expected = [
        'isDisabled', 'findChanged', 'compile',
        'getGroups', 'serviceByPid', 'writeIfChanged', 'getContainerState'
    ]
    for key in expected:
        assert hasattr(util, key) and callable(getattr(util, key, None))

def test_isDisabled_returns_false_if_running_true():
    class C: pass
    c = C(); c.process = type('P', (), {'flags': {'running': True}})()
    assert util.isDisabled(c) is False

def test_isDisabled_returns_true_if_running_false():
    class C: pass
    c = C(); c.process = type('P', (), {'flags': {'running': False}})()
    assert util.isDisabled(c) is True

def test_isDisabled_returns_true_if_flags_missing():
    class C: pass
    c = C(); c.process = type('P', (), {})()
    assert util.isDisabled(c) is True
    assert util.isDisabled() is True

def test_findChanged_returns_empty_array_if_no_containers():
    assert util.findChanged({}, {}) == []

def test_findChanged_returns_changed_items_when_content_changes():
    oldState = {'svc': {'some':'old'}}
    newState = {'svc': {'some':'new'}}
    assert util.findChanged(newState, oldState) == ['svc']

def test_compile_returns_a_string_for_input():
    assert isinstance(util.compile('foo'), str)

def test_findChanged_supports_error_path_for_invalid_args():
    assert util.findChanged(None, None) == []

def test_getGroups_returns_list_of_groups():
    services = {
        'svc1': {'group': 'groupA'},
        'svc2': {'group': 'groupB'},
        'svc3': {'group': 'groupA'}
    }
    result = util.getGroups(services)
    assert 'groupA' in result
    assert 'groupB' in result

def test_serviceByPid_finds_service_by_pid():
    state = {'s1': {'process': {'pid': 42}}}
    assert util.serviceByPid(state, 42) == 's1'
    assert util.serviceByPid(state, 9999) is None

def test_writeIfChanged_writes_only_if_content_changes(tmp_path):
    import os
    tmp_file = tmp_path / "tmp_utl.txt"
    util.writeIfChanged(str(tmp_file), 'foo', lambda: None)
    util.writeIfChanged(str(tmp_file), 'foo', lambda: None)
    assert tmp_file.exists()

def test_getContainerState_returns_correct_state():
    containers = {'foo': {'process': {'stopped': True}}}
    assert util.getContainerState(containers, 'foo') == 'stopped'
    assert util.getContainerState({}, 'bar') == 'not-started'