import pytest
from src.path_planning.obstacles import Obstacles

def test_add_and_size_different():
    obs = Obstacles()
    assert obs.size() == 0
    obs.addObstacle(-2, -2, 3)
    assert obs.size() == 1

def test_collision_positive_offset():
    obs = Obstacles()
    obs.addObstacle(2, -2, 2)
    assert obs.isColliding(4, -2)
    assert obs.isColliding(2, 0)
    assert obs.isColliding(2, -4)

def test_collision_negative_far():
    obs = Obstacles()
    obs.addObstacle(10, 10, 2)
    assert not obs.isColliding(15, 15)
    assert not obs.isColliding(0, 0)

def test_multiple_obstacles_far():
    obs = Obstacles()
    obs.addObstacle(4, 5, 1.5)
    obs.addObstacle(-4, -5, 2.5)
    assert obs.isColliding(4, 6.5)
    assert not obs.isColliding(20, 20)