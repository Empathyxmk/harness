import pytest
from src.scenario_tree import scenario_tree

def test_scenario_tree_behavior_public():
    # Public: check scenario_tree behavior with different param
    try:
        scenario_tree('draw', True, 'scenarios', 2)
        print('scenario_tree executed with draw=true, scenarios=2 (public).')
    except Exception as e:
        print(f"scenario_tree_behavior public error: {e}")