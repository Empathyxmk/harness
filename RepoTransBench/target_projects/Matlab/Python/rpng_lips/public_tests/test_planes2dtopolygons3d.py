import pytest
import numpy as np

from src.lips.planes2dtopolygons3d import planes2dtopolygons3d

def test_polygon_different_plane_height():
    poly2d = [np.array([[1, 1], [2, 1], [2, 2], [1, 2]])]
    planeheight = 5.5
    polys3d = planes2dtopolygons3d(poly2d, planeheight)
    assert len(polys3d) == 1
    assert polys3d[0].shape[1] == 3
    # The unique z values in third column should be [0, planeheight]
    assert np.all(np.isin(np.unique(polys3d[0][:, 2]), [0, planeheight]))

def test_multiple_2d_polygons_public():
    poly2d = [
        np.array([[1, 2], [5, 2], [5, 3], [1, 3]]),
        np.array([[6, 7], [9, 7], [9, 8], [6, 8]])
    ]
    planeheight = 3.3
    polys3d = planes2dtopolygons3d(poly2d, planeheight)
    assert len(polys3d) == 2