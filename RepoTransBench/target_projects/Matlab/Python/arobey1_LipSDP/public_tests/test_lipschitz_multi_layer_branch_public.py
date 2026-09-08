import pytest
import numpy as np
from src.lipsdp.lipschitz_multi_layer import lipschitz_multi_layer

def test_invalid_mode_branches_nested_public():
    w = [[np.eye(4), np.eye(4)]]
    network = {'alpha': 0.75, 'beta': 3.0, 'weight_path': ['some_path']}
    with pytest.raises(ValueError, match="formulation must be in"):
        lipschitz_multi_layer(w, 'nonsense_mode', False, 4, 5, [4,4,4], network)