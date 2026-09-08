import os
import pytest

TEST_CASADI_CODE1_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MPC_code', 'casadi_code1')
TEST_CASADI_CODE2_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'MPC_code', 'casadi_code2')

def test_Graph_MPC_casadi_exists_in_code1_public():
    fpath = os.path.join(TEST_CASADI_CODE1_PATH, 'Graph_MPC_casadi.m')
    assert os.path.isfile(fpath), "Graph_MPC_casadi.m not in casadi_code1"

def test_Graph_MPC_casadi_exists_in_code2_public():
    fpath = os.path.join(TEST_CASADI_CODE2_PATH, 'Graph_MPC_casadi.m')
    assert os.path.isfile(fpath), "Graph_MPC_casadi.m not in casadi_code2"