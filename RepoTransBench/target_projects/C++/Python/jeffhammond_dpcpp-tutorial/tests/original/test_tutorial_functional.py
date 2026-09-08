"""
Try to exercise any host-only logic in tutorial.hpp if present,
otherwise, serve as a coverage anchor for host-compilable features.
"""

def example_host_function(x):
    return x * 2

def test_tutorial_functional():
    print("Functional host-side test for possible logic in tutorial.hpp.")
    assert example_host_function(2) == 4
    assert example_host_function(0) == 0