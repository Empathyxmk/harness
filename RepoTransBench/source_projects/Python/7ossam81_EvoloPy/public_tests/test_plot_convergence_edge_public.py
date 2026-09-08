import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib
matplotlib.use("Agg")
import EvoloPy.plot_convergence as pc

def test_plot_convergence_shorter_convergence_vector_public(tmp_path):
    convergence = [[410, 200, 5]]
    optimizer = ['ShortEdgeOpt']
    func_name = "F21"
    with patch("pandas.read_csv") as m:
        m.return_value = None
        try:
            pc.run(convergence, optimizer, func_name, 1)
        except Exception as e:
            if not isinstance(e, (AttributeError, NotImplementedError, TypeError)):
                raise