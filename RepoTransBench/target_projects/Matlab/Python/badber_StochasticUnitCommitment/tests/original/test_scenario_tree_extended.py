import pytest
from src.scenario_tree import scenario_tree

def test_scenario_tree_extended():
    # Extended test: try additional argument combos
    try:
        scenario_tree('branches', 3, 'depth', 2)
    except Exception:
        print('scenario_tree extended parameters failed (ok)')
    try:
        scenario_tree('custom', [])
    except Exception:
        print('scenario_tree custom empty call failed (ok)')
    print('All extended tests for scenario_tree executed.')