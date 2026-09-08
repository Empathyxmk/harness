import pytest
from src.path_planning.obstacles import obstacles, geometry_msgs

def test_initializeBoundaryPublic():
    bondArray = []
    point = geometry_msgs.Point()
    point.x = 10; point.y = 10; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 10; point.y = 50; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 50; point.y = 50; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 50; point.y = 10; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    point.x = 10; point.y = 10; point.z = 0; bondArray.append(geometry_msgs.Point(point.x, point.y, point.z))
    return bondArray

def test_initializeObstaclesPublic():
    obj = obstacles()
    obstArray = obj.getObstacleArray()
    obstaclesMarker = []
    for i in range(len(obstArray)):
        for j in range(1, 5):
            obstaclesMarker.append(obstArray[i][j-1])
            obstaclesMarker.append(obstArray[i][j])
    # Instead of relying on the default, let's change a value for test
    if obstaclesMarker:
        obstaclesMarker[0].x += 10
    return obstaclesMarker

def test_boundary_initialization_public():
    bounds = test_initializeBoundaryPublic()
    assert len(bounds) == 5
    assert bounds[0].x == pytest.approx(10)
    assert bounds[1].y == pytest.approx(50)
    assert bounds[2].x == pytest.approx(50)
    assert bounds[3].y == pytest.approx(10)
    assert bounds[4].x == pytest.approx(10)

def test_obstacles_initialization_public():
    markers = test_initializeObstaclesPublic()
    assert len(markers) == 8
    assert markers[0].x == pytest.approx(60)
    if len(markers) > 1:
        assert abs(markers[1].y - 70) < 1e-5

def test_idempotent_get_obstacle_array_public():
    o1 = obstacles()
    o2 = obstacles()
    arr1 = o1.getObstacleArray()
    arr2 = o2.getObstacleArray()
    assert len(arr1) == 1
    assert len(arr2) == 1
    assert len(arr1[0]) == 5
    assert len(arr2[0]) == 5
    for i in range(5):
        assert arr1[0][i].x == arr2[0][i].x