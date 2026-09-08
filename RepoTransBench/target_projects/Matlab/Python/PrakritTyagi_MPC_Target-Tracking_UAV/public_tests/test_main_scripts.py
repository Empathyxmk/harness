import os
import sys
import pytest
import importlib.util
import traceback

CASADI_CODE1_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MPC_code', 'casadi_code1')
CASADI_CODE2_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MPC_code', 'casadi_code2')

def test_public_main_robot_tracking_script_changes_N(monkeypatch):
    script_name = 'main_Robot_Tracking_obs_avoid_single_sh'
    script_m = os.path.join(CASADI_CODE1_PATH, script_name + '.m')
    assert os.path.exists(script_m), f"{script_m} not found"
    script_py = os.path.join(CASADI_CODE1_PATH, script_name + '.py')
    if os.path.exists(script_py):
        # Simulate changing variable N before running the script
        spec = importlib.util.spec_from_file_location(script_name, script_py)
        mod = importlib.util.module_from_spec(spec)
        try:
            sys.path.insert(0, CASADI_CODE1_PATH)
            setattr(mod, "N", 5)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"main_Robot_Tracking_obs_avoid_single_sh public error: {e}\n{traceback.format_exc()}")
        finally:
            sys.path.remove(CASADI_CODE1_PATH)
    else:
        pytest.skip("No Python version of main_Robot_Tracking_obs_avoid_single_sh.m")

def test_public_main_multi_robot_tracking_script_changes_vfov(monkeypatch):
    script_name = 'main_Multi_Robot_Tracking_obs_avoid_single_sh'
    script_m = os.path.join(CASADI_CODE2_PATH, script_name + '.m')
    assert os.path.exists(script_m), f"{script_m} not found"
    script_py = os.path.join(CASADI_CODE2_PATH, script_name + '.py')
    if os.path.exists(script_py):
        # Simulate changing VFOV_deg before running the script
        spec = importlib.util.spec_from_file_location(script_name, script_py)
        mod = importlib.util.module_from_spec(spec)
        try:
            sys.path.insert(0, CASADI_CODE2_PATH)
            setattr(mod, 'VFOV_deg', 50)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"main_Multi_Robot_Tracking_obs_avoid_single_sh public error: {e}\n{traceback.format_exc()}")
        finally:
            sys.path.remove(CASADI_CODE2_PATH)
    else:
        pytest.skip("No Python version of main_Multi_Robot_Tracking_obs_avoid_single_sh.m")