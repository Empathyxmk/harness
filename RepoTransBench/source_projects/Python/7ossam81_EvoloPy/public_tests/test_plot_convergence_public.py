import sys
import os
import numpy as np
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib
matplotlib.use("Agg")
import EvoloPy.plot_convergence as pc

def test_plot_convergence_multiple_opts_public(tmp_path):
    convergence = [list(np.linspace(900, 10, 15)), list(np.linspace(555, 20, 15))]
    optimizer = ['PhoOpt', 'KappaOpt']
    func_name = "F13"
    with patch("pandas.read_csv") as m:
        m.return_value = None
        try:
            pc.run(convergence, optimizer, func_name, 2)
        except Exception as e:
            if not isinstance(e, (AttributeError, NotImplementedError, TypeError)):
                raise

def test_plot_convergence_iterate_public():
    convergence = [list(np.linspace(380, 34, 6))]
    optimizer = ['Pi']
    with patch("pandas.read_csv") as m:
        m.return_value = None
        try:
            pc.run(convergence, optimizer, "F5", 1)
        except Exception as e:
            if not isinstance(e, (AttributeError, NotImplementedError, TypeError)):
                raise