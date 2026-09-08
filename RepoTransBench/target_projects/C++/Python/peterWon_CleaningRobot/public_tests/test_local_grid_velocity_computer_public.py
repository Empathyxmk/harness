import math
from src.local_grid_velocity_computer import LocalGridVelocityComputer
from src.geometry_msgs import Pose

def test_different_velocity_computation():
    comp = LocalGridVelocityComputer()

    robot_pose = Pose()
    robot_pose.position.x = 5.0
    robot_pose.position.y = 3.0

    goal_pose = Pose()
    goal_pose.position.x = 7.5
    goal_pose.position.y = 3.0

    linear = [None]
    angular = [None]
    comp.computeVelocityCommand(robot_pose, goal_pose, linear, angular, 2.0)
    assert math.isclose(linear[0], 2.5, abs_tol=1e-4)
    assert math.isclose(angular[0], 0.0, abs_tol=1e-4)

    # Check not a straight line
    goal_pose.position.x = 5.0
    goal_pose.position.y = 6.0
    comp.computeVelocityCommand(robot_pose, goal_pose, linear, angular, 1.0)
    assert math.isclose(linear[0], 3.0, abs_tol=1e-4)
    assert not math.isclose(angular[0], 0.0, abs_tol=1e-7)

def test_already_at_goal_new_data():
    comp = LocalGridVelocityComputer()
    robot_pose = Pose()
    robot_pose.position.x = 4.2
    robot_pose.position.y = -1.1
    goal_pose = Pose()
    goal_pose.position.x = 4.2
    goal_pose.position.y = -1.1
 
    linear = [None]
    angular = [None]
    comp.computeVelocityCommand(robot_pose, goal_pose, linear, angular, 1.5)
    assert math.isclose(linear[0], 0.0, abs_tol=1e-4)
    assert math.isclose(angular[0], 0.0, abs_tol=1e-4)