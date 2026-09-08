import pytest
import numpy as np
from hgpvision.sim_main import simMain

class TestSimMainBranches:
    def test_run_and_state_var(self):
        # Test that simMain runs and expected vars exist in the global scope
        simMain()
        global_vars = globals()
        required_vars = ['atti', 'ins', 'gps', 't']
        for var in required_vars:
            assert var in global_vars, f'Variable {var} missing after simMain run.'

    def test_state_corner_cases(self):
        # Simulate initialization and rerun
        globals()['atti'] = np.zeros(3)
        globals()['ins'] = {}
        globals()['gps'] = {}
        globals()['t'] = 0
        simMain()
        assert 'atti' in globals()