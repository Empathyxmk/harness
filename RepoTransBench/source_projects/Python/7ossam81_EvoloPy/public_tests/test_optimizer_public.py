import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from EvoloPy.optimizer import selector, run

def test_selector_with_custom_algorithm_public():
    details = ['F16',-100, 100, 4]
    result = selector('GWO', details, 6, 3)
    assert hasattr(result, 'fitness') or hasattr(result, 'convergence')

def test_selector_invalid_name_public():
    details = ['F2',-50, 50, 2]
    result = selector('UNKNOWN_PUBLIC', details, 5, 5)
    assert result is None or result is False

def test_run_multiple_algo_public():
    details = [['F12', -100, 100, 6]]
    algos = ['WOA', 'HHO']
    # Corrected: run expects (optimizer, objectivefunc, params, export_flags)
    params = {"PopulationSize": 2, "Iterations": 2}
    export_flags = [False, False, False, False]
    run(algos, details, params, export_flags)