import pytest

from lihongbo_consensus.consensus_APF import consensus_APF
from lihongbo_consensus.consensus_DWA import consensus_DWA

def test_consensus_APF_basic():
    # Example input and expected output. Adjust as needed for your actual function signature and logic.
    input_params = {
        "position": [1.0, 2.0, 3.0],
        "target": [4.0, 5.0, 6.0],
        "repulsion": [0.2, 0.2, 0.2]
    }
    # The following call and check are demonstrative.
    result = consensus_APF(**input_params)
    assert isinstance(result, dict)
    assert "force" in result
    assert all(isinstance(x, float) for x in result["force"])

def test_consensus_DWA_basic():
    # Example input and expected output. Adjust as needed for your actual function signature and logic.
    input_params = {
        "x": 2.0,
        "y": 3.0,
        "theta": 0.5,
        "goal": [5.0, 6.0],
        "obstacles": [[1.0, 2.0], [3.0, 4.0]]
    }
    result = consensus_DWA(**input_params)
    assert "trajectory" in result
    assert isinstance(result["trajectory"], list)
    assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in result["trajectory"])