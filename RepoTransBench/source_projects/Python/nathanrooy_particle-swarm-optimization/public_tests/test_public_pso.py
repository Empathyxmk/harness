import sys
import os

# Ensure pso is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pso.pso_simple as pso_simple
import pso.cost_functions as cost_functions

def test_minimize_with_sphere_function_public():
    x0 = [-2.0, 3.0]
    bounds = [(-10, 10), (-10, 10)]
    err, pos = pso_simple.minimize(cost_functions.sphere, x0, bounds, num_particles=5, maxiter=12)
    assert err <= cost_functions.sphere(x0)
    assert len(pos) == len(x0)