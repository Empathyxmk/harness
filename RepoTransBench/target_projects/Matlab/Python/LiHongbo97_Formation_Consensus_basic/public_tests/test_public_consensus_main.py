import pytest

from lihongbo_consensus.consensus_APF import consensus_APF
from lihongbo_consensus.consensus_DWA import consensus_DWA

def test_public_consensus_APF_valid():
    input_params = {
        "position": [2.0, 3.0, 4.0],
        "target": [7.0, 8.0, 9.0],
        "repulsion": [0.1, 0.1, 0.1]
    }
    result = consensus_APF(**input_params)
    assert isinstance(result, dict)
    assert "force" in result
    assert all(isinstance(x, float) for x in result["force"])

def test_public_consensus_DWA_valid():
    input_params = {
        "x": 1.0,
        "y": 2.0,
        "theta": 0.7,
        "goal": [9.0, 7.0],
        "obstacles": [[3.0, 3.0], [4.0, 5.0]]
    }
    result = consensus_DWA(**input_params)
    assert "trajectory" in result
    assert isinstance(result["trajectory"], list)
    assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in result["trajectory"])