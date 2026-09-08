import pytest
from src.path_planning.obstacles import Obstacles

def test_add_and_size():
    obs = Obstacles()
    assert obs.size() == 0
    obs.addObstacle(1, 1, 1)
    assert obs.size() == 1

def test_collision_positive():
    obs = Obstacles()
    obs.addObstacle(0, 0, 1)
    assert obs.isColliding(0, 0)
    assert obs.isColliding(1, 0)
    assert obs.isColliding(-1, 0)

def test_collision_negative():
    obs = Obstacles()
    obs.addObstacle(0, 0, 1)
    assert not obs.isColliding(2, 2)
    assert not obs.isColliding(-2, -2)

def test_multiple_obstacles():
    obs = Obstacles()
    obs.addObstacle(0, 0, 1)
    obs.addObstacle(2, 2, 1)
    assert obs.isColliding(2, 2)
    assert not obs.isColliding(10, 10)