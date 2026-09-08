import os
import numpy as np
from src.bfm_landmarks.landmarks import read_landmarks

def test_public_read_landmarks_21_anl():
    """
    Public test for reading landmarks (21 points).
    """
    fn = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "Landmarks21_BFM.anl")
    pts = read_landmarks(fn)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2 and pts.shape[1] == 2 and pts.shape[0] > 0, "Should be Nx2 matrix"

def test_public_read_landmarks_68_anl():
    """
    Public test for reading landmarks (68 points).
    """
    fn = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "Landmarks68_BFM.anl")
    pts = read_landmarks(fn)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2 and pts.shape[1] == 2 and pts.shape[0] > 0, "Should be Nx2 matrix"