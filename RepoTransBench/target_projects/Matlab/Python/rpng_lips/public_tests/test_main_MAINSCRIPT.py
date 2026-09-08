import pytest
import numpy as np

from src.lips.planes2dtopolygons3d import planes2dtopolygons3d

def test_main_script_runs_partial_public(tmp_path):
    # Use dummy data to simulate loading from test_planes2dtopolygons3d_dummydata.mat
    # S.planes2d = list of arrays (in .mat it's usually a dict)
    planes2d = [np.array([[1, 2], [2, 2], [2, 3], [1, 3]])]
    planeheight = 2.5
    try:
        polygons3d = planes2dtopolygons3d(planes2d, planeheight)
        assert True
    except Exception as ex:
        pytest.fail(f"main_MAINSCRIPT public test errored: {ex}")