# test_scatternet_public_extended.py
# Extended public test for ScatterNet with different focus
import os

def test_demo_sh_exists():
    # Confirm an auxiliary shell script exists as a public infrastructure check
    assert os.path.isfile("demo.sh"), "demo.sh should exist"

def test_spherical_tm1_exists():
    # Confirm a T-matrix function is present in the subdirectory
    target_path = os.path.join('spherical_T_matrix','spherical_TM1.m')
    assert os.path.isfile(target_path), "spherical_T_matrix/spherical_TM1.m should exist"