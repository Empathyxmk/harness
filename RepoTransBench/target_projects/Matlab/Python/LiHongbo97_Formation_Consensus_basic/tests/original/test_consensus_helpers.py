import pytest
from lihongbo_consensus.consensus_APF import consensus_APF
from lihongbo_consensus.consensus_DWA import consensus_DWA

def test_consensus_helpers_smoke():
    try:
        consensus_APF()
        consensus_DWA()
    except Exception:
        pytest.fail("Consensus helpers failed")