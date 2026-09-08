import sys
import os

# Ensure pso is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pso.pso_simple as pso_simple
import pso.cost_functions as cost_functions

def test_minimize_with_sphere_function():
    x0 = [1.0, 2.0]
    bounds = [(-5, 5), (-5, 5)]
    err, pos = pso_simple.minimize(cost_functions.sphere, x0, bounds, num_particles=4, maxiter=15)
    assert err <= cost_functions.sphere(x0)
    assert len(pos) == len(x0)