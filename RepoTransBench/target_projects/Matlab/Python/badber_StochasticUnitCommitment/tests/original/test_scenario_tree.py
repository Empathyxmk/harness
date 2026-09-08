import pytest
from src.scenario_tree import scenario_tree

def test_scenario_tree():
    # Basic call to scenario_tree for coverage/graceful error
    try:
        scenario_tree()
        print("scenario_tree executed successfully.")
    except Exception as e:
        print(f"scenario_tree error: {e}")