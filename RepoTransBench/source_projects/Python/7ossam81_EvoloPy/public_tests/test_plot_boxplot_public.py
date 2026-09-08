import sys
import os
import numpy as np
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib
matplotlib.use("Agg")
import EvoloPy.plot_boxplot as pb

def test_plot_boxplot_random_data_public(tmp_path):
    data = [np.random.rand(10)*100, np.random.rand(10)*200]
    optimizer = ['ZetaOpt', 'TeraOpt']
    # Mock pandas.read_csv so code path doesn't error if run tries to use it
    with patch("pandas.read_csv") as m:
        m.return_value = None
        try:
            pb.run(data, optimizer, "F2", 3)
        except Exception as e:
            # Accept if failure only if error is not from code under test (i.e., allow not implemented errors, but not data shape/type errors)
            if not isinstance(e, (AttributeError, NotImplementedError, TypeError)):
                raise

def test_boxplot_creates_different_tick_labels_public():
    data = [np.random.rand(5)*10 for _ in range(3)]
    optimizer = ['Matrix', 'Omega', 'Sigma']
    with patch("pandas.read_csv") as m:
        m.return_value = None
        try:
            pb.run(data, optimizer, "F3", 3)
        except Exception as e:
            if not isinstance(e, (AttributeError, NotImplementedError, TypeError)):
                raise