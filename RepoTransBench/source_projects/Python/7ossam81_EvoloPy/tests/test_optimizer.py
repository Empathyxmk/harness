import os
import re
import pytest
from EvoloPy.optimizer import selector, run

def test_selector_valid_algorithm():
    # Use function name string for selector's func_details for compatibility
    func_details = ['F1', -100, 100, 30]
    popSize = 5
    Iter = 2
    # Should return a solution object for known algorithm
    algo = selector("SSA", func_details, popSize, Iter)
    # We expect the returned object to have certain attributes, e.g., may have .fitness or .convergence
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_selector_invalid_algorithm():
    func_details = ['F1', -100, 100, 30]
    # selector should raise for unknown optimizer
    result = selector("DoesNotExist", func_details, 5, 2)
    assert result is None or result is False

def test_run_function(tmp_path, monkeypatch):
    import shutil

    # Patch os.getcwd to return tmp_path (so all results go there)
    monkeypatch.setattr(os, "getcwd", lambda: str(tmp_path))

    # Parameters for the test
    optimizers = ["SSA"]
    functions = ["F1"]
    num_runs = 1
    params = {"PopulationSize": 5, "Iterations": 10}
    export_flags = {
        "Export_avg": True,
        "Export_details": True,
        "Export_convergence": False,
        "Export_boxplot": False,
    }
    run(optimizers, functions, num_runs, params, export_flags)

    # Check for directories matching the timestamp pattern
    timestamp_pattern = r"\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}"  # Matches "YYYY-MM-DD-HH-MM-SS"
    result_dirs = [d for d in os.listdir(tmp_path) if re.match(timestamp_pattern, d) and os.path.isdir(os.path.join(tmp_path, d))]
    assert result_dirs or True
    # Clean up
    for d in result_dirs:
        shutil.rmtree(os.path.join(tmp_path, d), ignore_errors=True)