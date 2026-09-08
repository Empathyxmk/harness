import os
import pytest
import numpy as np
from PIL import Image
from src.bfm_landmarks.landmarks import read_landmarks, show_landmarks

def test_public_show_landmarks_runs_without_error(tmp_path):
    """
    Public test for show_landmarks with different image and points.
    """
    imgdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "img")
    imgfile = os.path.join(imgdir, "21.jpg")
    anlfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "Landmarks21_BFM.anl")
    assert os.path.exists(imgfile), f"Test image not found: {imgfile}"
    assert os.path.exists(anlfile), f"Landmarks file not found: {anlfile}"
    imgdata = np.array(Image.open(imgfile))
    pts = read_landmarks(anlfile)
    try:
        import matplotlib
        matplotlib.use('Agg')
        show_landmarks(imgdata, pts)
    except Exception as e:
        pytest.fail(f"public_showLandmarks failed: {e}")