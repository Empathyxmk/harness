import sys
import os

# Ensure pso is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pso import pso_simple

def public_cost(x):
    return sum(val ** 2 for val in x) + 1  # Slightly different for variety

def test_particle_instance_and_attributes_public():
    x0 = [7, -3, 2]
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

def test_particle_evaluate_and_personal_best_public():
    x0 = [5, 6]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    p.evaluate(public_cost)
    err_first = p.err_best_i
    # evaluate with new position
    p.position_i = [1, 2]
    p.evaluate(public_cost)
    assert p.err_best_i == err_first or p.err_best_i == public_cost([1, 2])  # accept either, if new error is better
    assert p.err_i == public_cost([1, 2])

def test_particle_update_velocity_and_position_public():
    x0 = [0.75, -0.25, 0.50]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    p.pos_best_i = x0.copy()
    pos_best_g = [0.0, 0.5, -0.5]
    old_v = p.velocity_i.copy()
    p.update_velocity(pos_best_g)
    assert len(p.velocity_i) == len(old_v)

    bounds = [(-2, 2), (-2, 2), (-2, 2)]
    # artificially set velocity large to test bounds
    p.velocity_i = [3, -3, 4]
    p.update_position(bounds)
    assert all(-2 <= v <= 2 for v in p.position_i)

def test_minimize_basic_public():
    x0 = [2, -3, 1]
    bounds = [(-7, 7), (-7, 7), (-7, 7)]
    err, pos = pso_simple.minimize(public_cost, x0, bounds, num_particles=4, maxiter=8, verbose=False)
    assert isinstance(err, float)
    assert isinstance(pos, list)
    assert len(pos) == len(x0)

def test_minimize_verbose_output_public(capsys):
    x0 = [-1, 1]
    bounds = [(-2, 2), (-2, 2)]
    err, pos = pso_simple.minimize(public_cost, x0, bounds, num_particles=3, maxiter=2, verbose=True)
    captured = capsys.readouterr()
    assert "iter:" in captured.out
    assert "FINAL SOLUTION" in captured.out

def test_minimize_edge_case_zero_iterations_public():
    x0 = [6, 8]
    bounds = [(-20, 20), (-20, 20)]
    global num_dimensions
    num_dimensions = len(x0)
    err, pos = pso_simple.minimize(public_cost, x0, bounds, num_particles=2, maxiter=0)
    assert isinstance(err, (float, int))
    assert isinstance(pos, list)

def test_update_position_hits_upper_bound_public():
    x0 = [0.7, 0.4]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    bounds = [(0, 1), (0, 1)]
    # set velocity so position[1] will go above upper bound
    p.velocity_i = [0.0, 0.8]
    p.update_position(bounds)
    assert p.position_i[1] == 1.0
    assert p.position_i[0] == x0[0] + p.velocity_i[0]

def test_update_position_hits_lower_bound_public():
    x0 = [-0.8, 0.2]
    global num_dimensions
    num_dimensions = len(x0)
    p = pso_simple.Particle(x0)
    bounds = [(-1, 0), (-1, 0)]
    p.velocity_i = [-0.5, 0.0]  # only move the first dimension
    p.update_position(bounds)
    assert p.position_i[0] == -1.0
    assert p.position_i[1] == x0[1] + p.velocity_i[1]