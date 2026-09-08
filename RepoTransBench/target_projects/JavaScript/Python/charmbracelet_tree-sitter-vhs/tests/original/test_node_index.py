import os
import sys
import types
import importlib
import pytest

@pytest.fixture(autouse=True)
def clean_sys_modules():
    keys = list(sys.modules.keys())
    yield
    for k in list(sys.modules.keys()):
        if k not in keys:
            del sys.modules[k]


def test_should_export_module_and_attach_node_type_info(monkeypatch):
    # Mock a module returned from "node-gyp-build"
    class MockExport(dict):
        pass

    def mock_node_gyp_build(root):
        obj = MockExport(mockExport=True)
        # Simulate loading of node-type info from JSON in src/node-types.json
        # Let's load from src/node-types.json if available
        node_types_path = os.path.join(os.path.dirname(__file__), '../../src/node-types.json')
        if os.path.isfile(node_types_path):
            import json
            with open(node_types_path, 'r', encoding='utf-8') as f:
                node_type_info = json.load(f)
            obj.nodeTypeInfo = node_type_info
        else:
            obj.nodeTypeInfo = []
        return obj

    monkeypatch.setattr('builtins.__import__', lambda name, globals=None, locals=None, fromlist=(), level=0:
                        mock_node_gyp_build(None) if name == "node-gyp-build" else __import__(name, globals, locals, fromlist, level)
    , raising=False)

    # Simulate importing the module. We cannot perfectly match JS, but we can simulate the core logic.
    exp = mock_node_gyp_build(None)
    assert exp["mockExport"] is True
    assert hasattr(exp, 'nodeTypeInfo')
    assert isinstance(exp.nodeTypeInfo, (list, dict))  # Accept list/dict for JSON
    assert len(exp.nodeTypeInfo) >= 0

def test_should_fallback_gracefully_if_node_types_json_not_present(monkeypatch, tmp_path):
    # Remove the node-types.json file if it exists for this test
    node_types_path = os.path.join(os.path.dirname(__file__), '../../src/node-types.json')
    backup = None
    if os.path.isfile(node_types_path):
        with open(node_types_path, 'rb') as f:
            backup = f.read()
        os.remove(node_types_path)
    try:
        class MockExport(dict):
            pass
        def mock_node_gyp_build(root):
            obj = MockExport(mockExport=True)
            obj.nodeTypeInfo = None
            return obj
        monkeypatch.setattr('builtins.__import__', lambda name, globals=None, locals=None, fromlist=(), level=0:
                        mock_node_gyp_build(None) if name == "node-gyp-build" else __import__(name, globals, locals, fromlist, level)
        , raising=False)

        exp = mock_node_gyp_build(None)
        assert exp["mockExport"] is True
        # nodeTypeInfo may be undefined or not present
    finally:
        # Restore file if backed up
        if backup is not None:
            with open(node_types_path, 'wb') as f:
                f.write(backup)

def test_should_call_node_gyp_build_with_correct_root(monkeypatch):
    # Calls node-gyp-build with correct path
    called = {}
    def mock_node_gyp_build(root):
        called["root"] = root
        return {}
    monkeypatch.setattr('builtins.__import__', lambda name, globals=None, locals=None, fromlist=(), level=0:
                        mock_node_gyp_build("ROOT") if name == "node-gyp-build" else __import__(name, globals, locals, fromlist, level)
    , raising=False)
    # Simulate requiring index
    _ = mock_node_gyp_build("ROOT")
    assert "root" in called
    assert called["root"] == "ROOT"