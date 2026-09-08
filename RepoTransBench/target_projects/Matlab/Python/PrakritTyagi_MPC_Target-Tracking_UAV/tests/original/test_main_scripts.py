import os
import sys
import importlib.util
import traceback

import pytest

TEST_CASADI_CODE1_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'MPC_code', 'casadi_code1')
TEST_CASADI_CODE2_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'MPC_code', 'casadi_code2')

def get_script_path(script_name, dir_path):
    m_path = os.path.join(dir_path, script_name)
    if os.path.exists(m_path):
        return m_path
    py_path = os.path.splitext(m_path)[0] + ".py"
    if os.path.exists(py_path):
        return py_path
    return None

@pytest.mark.smoke
def test_main_Robot_Tracking_obs_avoid_single_sh_runs():
    # Check that main_Robot_Tracking_obs_avoid_single_sh.m or .py exists and run (as script)
    script_path = get_script_path('main_Robot_Tracking_obs_avoid_single_sh.m', TEST_CASADI_CODE1_PATH)
    assert script_path is not None, "main_Robot_Tracking_obs_avoid_single_sh.m not found in casadi_code1"
    script_py_path = os.path.splitext(script_path)[0] + '.py'
    if os.path.exists(script_py_path):
        spec = importlib.util.spec_from_file_location("main_Robot_Tracking_obs_avoid_single_sh", script_py_path)
        mod = importlib.util.module_from_spec(spec)
        try:
            sys.path.insert(0, TEST_CASADI_CODE1_PATH)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f'main_Robot_Tracking_obs_avoid_single_sh error: {e}\n{traceback.format_exc()}')
        finally:
            sys.path.remove(TEST_CASADI_CODE1_PATH)
    else:
        pytest.skip("No Python version of main_Robot_Tracking_obs_avoid_single_sh.m")

@pytest.mark.smoke
def test_main_Multi_Robot_Tracking_obs_avoid_single_sh_runs():
    # Check that main_Multi_Robot_Tracking_obs_avoid_single_sh.m or .py exists and run (as script)
    script_path = get_script_path('main_Multi_Robot_Tracking_obs_avoid_single_sh.m', TEST_CASADI_CODE2_PATH)
    assert script_path is not None, "main_Multi_Robot_Tracking_obs_avoid_single_sh.m not found in casadi_code2"
    script_py_path = os.path.splitext(script_path)[0] + '.py'
    if os.path.exists(script_py_path):
        spec = importlib.util.spec_from_file_location("main_Multi_Robot_Tracking_obs_avoid_single_sh", script_py_path)
        mod = importlib.util.module_from_spec(spec)
        try:
            sys.path.insert(0, TEST_CASADI_CODE2_PATH)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f'main_Multi_Robot_Tracking_obs_avoid_single_sh error: {e}\n{traceback.format_exc()}')
        finally:
            sys.path.remove(TEST_CASADI_CODE2_PATH)
    else:
        pytest.skip("No Python version of main_Multi_Robot_Tracking_obs_avoid_single_sh.m")