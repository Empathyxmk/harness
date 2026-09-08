import pytest
from potpourri3d import point_cloud

@pytest.fixture
def points():
    return [[1,2,3],[0,0,0],[6,5,4],[3,2,1]]

def test_knn_public(points):
    nn = point_cloud.knn_search(points, points, 3)
    assert len(nn) == len(points)
    for indices in nn:
        assert len(indices) == 3

def test_radius_public(points):
    nn = point_cloud.radius_search(points, points, 5.0)
    assert all(len(i) >= 1 for i in nn)