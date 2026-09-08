from src.cleaning_path_planner import CleaningPathPlanner
from src.geometry_msgs import PoseStamped
from src.nav_msgs import Path

def test_cleaning_path_planner_diff_ref():
    planner = CleaningPathPlanner()
    start = PoseStamped()
    goal = PoseStamped()
    path = Path()
    # Different objects: should return True and populate path.dummy
    result = planner.planPath(start, goal, path)
    assert result is True
    assert path.dummy != []

def test_cleaning_path_planner_same_ref():
    planner = CleaningPathPlanner()
    start = PoseStamped()
    p2 = Path()
    # Same reference: should return False and leave p2.dummy empty (as by logic - only touched on success)
    same_result = planner.planPath(start, start, p2)
    assert same_result is False