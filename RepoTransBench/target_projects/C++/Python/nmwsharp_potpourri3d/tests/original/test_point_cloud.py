import pytest
from potpourri3d import point_cloud

@pytest.fixture
def points():
    return [[0,0,0],[1,1,1],[2,2,2],[3,3,3]]

def test_knn(points):
    nn = point_cloud.knn_search(points, points, 2)
    assert len(nn) == len(points)
    for indices in nn:
        assert len(indices) == 2

def test_radius(points):
    nn = point_cloud.radius_search(points, points, 2.0)
    assert all(len(i) >= 1 for i in nn)