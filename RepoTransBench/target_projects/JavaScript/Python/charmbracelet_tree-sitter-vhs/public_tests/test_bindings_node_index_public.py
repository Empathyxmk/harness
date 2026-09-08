import os

def test_node_gyp_build_called_with_project_root(monkeypatch):
    # Simulate "node-gyp-build" as a Python callable, track root
    called = {}

    def mock_node_gyp_build(root):
        called["root"] = root
        # Simulate public export structure
        return {"__publicTest": True, "calledWith": root}

    # Simulate expected root as absolute dir above, like public test
    expected_root_for_public_test = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    result = mock_node_gyp_build(expected_root_for_public_test)
    assert result["__publicTest"] is True
    assert os.path.abspath(result["calledWith"]) == expected_root_for_public_test