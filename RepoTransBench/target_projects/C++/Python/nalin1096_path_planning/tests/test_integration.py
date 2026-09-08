import pytest
from src.path_planning.obstacles import obstacles, geometry_msgs

# Helper for boundary for integration
def test_initializeBoundary():
    bondArray = []
    point = geometry_msgs.Point()
    point.x = 0; point.y = 0; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 0; point.y = 100; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 100; point.y = 100; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 100; point.y = 0; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 0; point.y = 0; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    return bondArray

def test_initializeObstacles():
    obj = obstacles()
    obstArray = obj.getObstacleArray()
    obstaclesMarker = []
    for i in range(len(obstArray)):
        for j in range(1, 5):
            obstaclesMarker.append(obstArray[i][j-1])
            obstaclesMarker.append(obstArray[i][j])
    return obstaclesMarker

def test_boundary_initialization():
    bounds = test_initializeBoundary()
    assert len(bounds) == 5
    assert bounds[0].x == pytest.approx(0)
    assert bounds[1].y == pytest.approx(100)
    assert bounds[2].x == pytest.approx(100)
    assert bounds[3].y == pytest.approx(0)
    assert bounds[4].x == pytest.approx(0)

def test_obstacles_initialization():
    markers = test_initializeObstacles()
    assert len(markers) == 8
    assert markers[0].x == pytest.approx(50)
    assert markers[1].y == pytest.approx(70)
    assert markers[2].x == pytest.approx(50)
    assert markers[3].x == pytest.approx(80)
    assert markers[4].y == pytest.approx(70)
    assert markers[7].x == pytest.approx(50)

def test_idempotent_get_obstacle_array():
    o1 = obstacles()
    o2 = obstacles()
    arr1 = o1.getObstacleArray()
    arr2 = o2.getObstacleArray()
    assert len(arr1) == 1
    assert len(arr2) == 1
    assert len(arr1[0]) == 5
    assert len(arr2[0]) == 5
    for i in range(5):
        assert arr1[0][i].y == arr2[0][i].y