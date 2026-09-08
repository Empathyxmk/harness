import pytest
from phamqv_woa_5g_communications.channelModel import channelModel

def test_channelModel_basic_behavior():
    snr_db = 20
    mod_scheme = "QPSK"
    nUsers = 2

    result = channelModel(snr_db, mod_scheme, nUsers)
    assert isinstance(result, dict)
    assert "BER" in result and "capacity" in result
    assert 0 <= result["BER"] <= 1
    assert result["capacity"] > 0