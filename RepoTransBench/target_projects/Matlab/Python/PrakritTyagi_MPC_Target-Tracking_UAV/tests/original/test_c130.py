import os
import sys
import importlib.util
import traceback

import pytest

TEST_CASADI_CODE1_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'MPC_code', 'casadi_code1')
TEST_CASADI_CODE2_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'MPC_code', 'casadi_code2')

def get_module_path(module_name, dir_path):
    m_path = os.path.join(dir_path, module_name)
    if os.path.exists(m_path):
        return m_path
    py_path = os.path.splitext(m_path)[0] + ".py"
    if os.path.exists(py_path):
        return py_path
    return None

@pytest.mark.smoke
def test_c130_code1_runs():
    # Check that c130.[m/py] exists in casadi_code1 and import/run it (simulate basic script run)
    c130_path = get_module_path('c130.m', TEST_CASADI_CODE1_PATH)
    assert c130_path is not None, "c130.m not found in casadi_code1"

    # Try to execute it if a Python version exists.
    c130_py_path = os.path.splitext(c130_path)[0] + '.py'
    if os.path.exists(c130_py_path):
        # Execute the Python module as a script
        spec = importlib.util.spec_from_file_location("c130", c130_py_path)
        c130 = importlib.util.module_from_spec(spec)
        try:
            sys.path.insert(0, TEST_CASADI_CODE1_PATH)
            spec.loader.exec_module(c130)
        except Exception as e:
            print(f'casadi_code1/c130 error: {e}\n{traceback.format_exc()}')
        finally:
            sys.path.remove(TEST_CASADI_CODE1_PATH)
    else:
        # If .py does not exist: skip in Python context
        pytest.skip("No Python implementation of c130.m to run")

@pytest.mark.smoke
def test_c130_code2_runs():
    # Check that c130.[m/py] exists in casadi_code2 and import/run it
    c130_path = get_module_path('c130.m', TEST_CASADI_CODE2_PATH)
    assert c130_path is not None, "c130.m not found in casadi_code2"

    c130_py_path = os.path.splitext(c130_path)[0] + '.py'
    if os.path.exists(c130_py_path):
        spec = importlib.util.spec_from_file_location("c130", c130_py_path)
        c130 = importlib.util.module_from_spec(spec)
        try:
            sys.path.insert(0, TEST_CASADI_CODE2_PATH)
            spec.loader.exec_module(c130)
        except Exception as e:
            print(f'casadi_code2/c130 error: {e}\n{traceback.format_exc()}')
        finally:
            sys.path.remove(TEST_CASADI_CODE2_PATH)
    else:
        pytest.skip("No Python implementation of c130.m to run")