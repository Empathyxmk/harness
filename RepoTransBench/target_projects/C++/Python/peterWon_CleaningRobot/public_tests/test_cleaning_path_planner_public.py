from src.cleaning_path_planner import CleaningPathPlanner

def test_path_plan_finds_path_different_scenario():
    # Grid: 4x4, free except for two obstacles
    grid = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ]
    planner = CleaningPathPlanner(grid)

    start = (3,0)
    goal = (0,3)
    path = planner.plan_path(start, goal)

    assert path, "Path should not be empty"
    assert path[0] == start, "Path should start at start"
    assert path[-1] == goal, "Path should end at goal"
    # Confirm path doesn't step on obstacles
    for pos in path:
        assert grid[pos[0]][pos[1]] == 0

def test_invalid_goal_returns_empty_for_new_data():
    # Grid: 3x3, surrounded goal
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    # Obstacle already at [1][1]
    planner = CleaningPathPlanner(grid)

    start = (0,0)
    goal = (1,1) # Obstacle

    path = planner.plan_path(start, goal)
    assert not path, "Path should be empty when goal is an obstacle"