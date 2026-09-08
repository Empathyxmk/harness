import pytest
import numpy as np
from src.lipsdp.lipschitz_multi_layer import lipschitz_multi_layer

def test_invalid_mode_branches():
    w = [[np.eye(2), np.eye(2)]]
    network = {'alpha': 0.1, 'beta': 1.0, 'weight_path': ['dummy']}
    with pytest.raises(ValueError, match="formulation must be in"):
        lipschitz_multi_layer(w, 'dummy', False, 1, 1, [2, 2, 2], network)