# test_scatternet.py
# Test basic ScatterNet functionality (template/smoke test)
import os

def test_scatter_net_py_exists():
    # Test that scatter_net.py (or equivalent pipeline) responds and exists
    # Smoke test, does not check deep correctness.
    assert os.path.isfile("scatter_net.py"), "scatter_net.py should exist"

def test_nn_m_exists():
    # Extra: test that NN.m exists too (Matlab/Octave main interface)
    assert os.path.isfile("NN.m"), "NN.m should exist"