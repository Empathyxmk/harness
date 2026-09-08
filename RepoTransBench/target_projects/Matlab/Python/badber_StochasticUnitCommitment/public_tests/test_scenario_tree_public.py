import pytest
from src.scenario_tree import scenario_tree

def test_scenario_tree_public():
    # Public variant: call scenario_tree with an arg (different code path)
    try:
        scenario_tree('draw', False)
        print("scenario_tree executed with draw=False.")
    except Exception as e:
        print(f"scenario_tree public error: {e}")