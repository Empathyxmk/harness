import os
import numpy as np
from src.bfm_landmarks.landmarks import read_landmarks

def test_read_landmarks_68_anl():
    """
    Test reading 68 point .anl landmark and its format.
    """
    fn = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "Landmarks68_BFM.anl")
    pts = read_landmarks(fn)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2 and pts.shape[1] == 2 and pts.shape[0] > 0, "68 landmarks: incorrect format"

def test_read_landmarks_21_anl():
    """
    Test reading 21 point .anl landmark and its format.
    """
    fn = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "Landmarks21_BFM.anl")
    pts = read_landmarks(fn)
    assert isinstance(pts, np.ndarray)
    assert pts.ndim == 2 and pts.shape[1] == 2 and pts.shape[0] > 0, "21 landmarks: incorrect format"