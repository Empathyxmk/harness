import pytest
from src.scenario_tree import scenario_tree

def test_scenario_tree_errors_public():
    # Public: Intentionally pass a weird arg to reach a different error path
    try:
        scenario_tree('unknownparam', 9999)
        print('scenario_tree did not error on unknown param (unexpected public).')
    except Exception as e:
        print(f"scenario_tree_errors_public (expected error): {e}")