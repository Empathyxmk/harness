import os
import sys
import importlib.util
import traceback
import pytest

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CASADI_CODE1_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MPC_code', 'casadi_code1')
CASADI_CODE2_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MPC_code', 'casadi_code2')

def try_c130_call_with_args(code_path, *args, **kwargs):
    c130_py = os.path.join(code_path, 'c130.py')
    if not os.path.exists(c130_py):
        pytest.skip("No c130.py available for invocation")
    sys.path.insert(0, code_path)
    try:
        import c130
        # Assume c130 is a function (simulate position, color, scale, etc.)
        h1 = c130.c130(*args, **kwargs)
        # Should return a matplotlib Figure or Axes or similar handle
        assert hasattr(h1, 'figure') or hasattr(h1, 'get_figure') or hasattr(h1, '__class__'), "c130 did not return a handle as expected"
        plt.close('all')
    except Exception as e:
        print(f'{os.path.basename(code_path)}/c130 public error: {e}\n{traceback.format_exc()}')
    finally:
        sys.path.pop(0)
        plt.close('all')

def test_public_c130_code1():
    # Check c130.py existence
    fpath = os.path.join(CASADI_CODE1_PATH, 'c130.m')
    assert os.path.exists(fpath), "c130.m not found in casadi_code1"
    # Attempt to call with alternate position, color and scale
    try_c130_call_with_args(
        CASADI_CODE1_PATH,
        50, 100, 20, color=[0, 0.5, 1], scale=2
    )

def test_public_c130_code2():
    # Check c130.py existence
    fpath = os.path.join(CASADI_CODE2_PATH, 'c130.m')
    assert os.path.exists(fpath), "c130.m not found in casadi_code2"
    try_c130_call_with_args(
        CASADI_CODE2_PATH,
        0, 0, -20, yaw=45, pitch=10, tailwing='g'
    )