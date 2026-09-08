import pytest
import numpy as np

import lafan1.extract as extract

def test_pad_and_concat_basic():
    arrs = [np.zeros((2,2)), np.ones((2,2))]
    result = extract.pad_and_concat(arrs, axis=0)
    assert result.shape == (4,2)
    assert (result[:2] == 0).all()
    assert (result[2:] == 1).all()

def test_pad_and_concat_different_shapes():
    arrs = [np.zeros((2,2)), np.ones((3,2))]
    result = extract.pad_and_concat(arrs, axis=0)
    assert result.shape == (5,2)

def test_flatten_dict():
    d = {"a": 1, "b": 2}
    keys, vals = extract.flatten_dict(d)
    assert set(keys) == {"a", "b"}
    assert set(vals) == {1,2}

def test_shape_returns_correct():
    arr = np.zeros((2, 3, 4))
    assert extract.shape(arr) == (2,3,4)
    arr = np.arange(6).reshape((2,3))
    assert extract.shape(arr) == (2,3)

def test_shape_empty():
    arr = np.empty((0, 2, 3))
    assert extract.shape(arr) == (0,2,3)

def test_parse_bvh_hierarchy_and_motion():
    text = '''
HIERARCHY
ROOT Hips
{
    OFFSET 0.00 0.00 0.00
    CHANNELS 6 Xposition Yposition Zposition Zrotation Xrotation Yrotation
    JOINT Knee
    {
        OFFSET 0.00 1.00 0.00
        CHANNELS 3 Zrotation Xrotation Yrotation
    }
}
MOTION
Frames: 2
Frame Time: 0.0333333
0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
1.0 1.0 1.0 0.5 0.5 0.5 0.1 0.2 0.3
'''
    parsed = extract.parse_bvh(text.split('\n'))
    assert "hierarchy" in parsed
    assert "motion" in parsed
    assert len(parsed["motion"]) == 2
    assert "channels" in parsed

def test_parse_bvh_malformed():
    with pytest.raises(Exception):
        extract.parse_bvh(["nonsense", "not bvh"])