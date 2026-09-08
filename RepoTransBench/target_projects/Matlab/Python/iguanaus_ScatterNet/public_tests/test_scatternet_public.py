# test_scatternet_public.py
# Public test for ScatterNet using different files for public evaluation
import os

def test_scatter_net_core_py_exists():
    # Test the presence of another core script (demonstration), NOT same as existing!
    assert os.path.isfile("scatter_net_core.py"), "scatter_net_core.py should exist"

def test_estimate_order_effects_m_exists():
    # Check for another interface: "estimateOrderEffects.m" exists
    assert os.path.isfile("estimateOrderEffects.m"), "estimateOrderEffects.m should exist"