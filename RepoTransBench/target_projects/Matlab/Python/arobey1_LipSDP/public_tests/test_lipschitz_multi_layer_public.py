import pytest
import numpy as np
from src.lipsdp.lipschitz_multi_layer import lipschitz_multi_layer

def test_invalid_mode_branches_public():
    w = [[np.eye(3), np.eye(3)]]
    network = {'alpha':0.5, 'beta':2.0, 'weight_path':['not_a_real_path']}
    with pytest.raises(ValueError, match="formulation must be in"):
        lipschitz_multi_layer(w, 'unknown_mode', False, 2, 3, [3,3,3], network)