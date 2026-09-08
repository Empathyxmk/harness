from src.local_grid_velocity_computer import LocalGridVelocityComputer
from src.geometry_msgs import Twist

def test_standard_velocity_computation():
    comp = LocalGridVelocityComputer()
    twist = Twist()
    comp.computeVelocity(1.5, -2.0, 0.3, twist)
    assert twist.linear.x == 1.5
    assert twist.linear.y == -2.0
    assert twist.angular.z == 0.3

def test_zero_theta():
    comp = LocalGridVelocityComputer()
    twist = Twist()
    comp.computeVelocity(0.7, 2.2, 0.0, twist)
    assert twist.linear.x == 0.7
    assert twist.linear.y == 2.2
    assert twist.angular.z == 0.0

def test_stop_velocity():
    comp = LocalGridVelocityComputer()
    twist = Twist()
    comp.computeVelocity(1,2,3,twist)
    comp.stopVelocity(twist)
    assert twist.linear.x == 0.0
    assert twist.linear.y == 0.0
    assert twist.angular.z == 0.0