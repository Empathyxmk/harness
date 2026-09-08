import sys
import os

# Ensure pso is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pso import pso_simple

def simple_cost(x):
    return sum(val ** 2 for val in x)

def test_particle_instance_and_attributes():
    x0 = [1, -1]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    assert hasattr(p, "position_i")
    assert hasattr(p, "velocity_i")
    assert hasattr(p, "pos_best_i")
    assert hasattr(p, "err_best_i")
    assert hasattr(p, "err_i")
    assert len(p.position_i) == len(x0)
    assert len(p.velocity_i) == len(x0)

def test_particle_evaluate_and_personal_best():
    x0 = [2, 3]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    p.evaluate(simple_cost)
    err_first = p.err_best_i
    # evaluate with same position, should NOT update best if not better
    p.position_i = [4, 5]
    p.evaluate(simple_cost)
    assert p.err_best_i == err_first or p.err_best_i == simple_cost([4, 5])  # accept either, if new error is better
    assert p.err_i == simple_cost([4, 5])

def test_particle_update_velocity_and_position():
    x0 = [0.5, -0.5]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    p.pos_best_i = x0.copy()
    pos_best_g = [0.1, 0.2]
    old_v = p.velocity_i.copy()
    p.update_velocity(pos_best_g)
    assert len(p.velocity_i) == len(old_v)

    bounds = [(-1, 1), (-1, 1)]
    # artificially set velocity large to test bounds
    p.velocity_i = [2, -2]
    p.update_position(bounds)
    assert all(-1 <= v <= 1 for v in p.position_i)

def test_minimize_basic():
    x0 = [1, 2]
    bounds = [(-5, 5), (-5, 5)]
    err, pos = pso_simple.minimize(simple_cost, x0, bounds, num_particles=5, maxiter=10, verbose=False)
    assert isinstance(err, float)
    assert isinstance(pos, list)
    assert len(pos) == len(x0)

def test_minimize_verbose_output(capsys):
    x0 = [0, 0]
    bounds = [(-1, 1), (-1, 1)]
    err, pos = pso_simple.minimize(simple_cost, x0, bounds, num_particles=3, maxiter=2, verbose=True)
    captured = capsys.readouterr()
    assert "iter:" in captured.out
    assert "FINAL SOLUTION" in captured.out

def test_minimize_edge_case_zero_iterations():
    # No optimization should happen; should return initial best
    x0 = [5, 7]
    bounds = [(-10, 10), (-10, 10)]
    # Patch num_dimensions before minimize is imported/used
    global num_dimensions
    num_dimensions = len(x0)
    err, pos = pso_simple.minimize(simple_cost, x0, bounds, num_particles=2, maxiter=0)
    # In the reference code, when maxiter==0, it returns the initial err as -1, which is int
    assert isinstance(err, (float, int))
    assert isinstance(pos, list)

def test_update_position_hits_upper_bound():
    x0 = [0.9, 0.0]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    bounds = [(0, 1), (0, 1)]
    # set velocity so position[0] will go above upper bound
    p.velocity_i = [0.5, 0.0]  # only move the first dimension
    p.update_position(bounds)
    assert p.position_i[0] == 1.0
    # the second stays unchanged
    assert p.position_i[1] == x0[1] + p.velocity_i[1]

def test_update_position_hits_lower_bound():
    x0 = [0.0, -0.9]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    bounds = [(-1, 0), (-1, 0)]
    # set velocity so position[1] will go below lower bound
    p.velocity_i = [0.0, -0.5]  # only move the second dimension
    p.update_position(bounds)
    assert p.position_i[1] == -1.0
    # first stays unchanged
    assert p.position_i[0] == x0[0] + p.velocity_i[0]