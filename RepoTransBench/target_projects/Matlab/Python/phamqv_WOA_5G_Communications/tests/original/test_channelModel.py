import pytest
from phamqv_woa_5g_communications.channelModel import channelModel

def test_channelModel_output_range():
    snr_db = 15
    mod_scheme = "16QAM"
    nUsers = 3

    out = channelModel(snr_db, mod_scheme, nUsers)
    assert "BER" in out and "capacity" in out
    assert 0 <= out["BER"] <= 1
    assert out["capacity"] > 0

def test_channelModel_invalid_mod_scheme():
    snr_db = 10
    mod_scheme = "INVALID"
    nUsers = 1

    try:
        channelModel(snr_db, mod_scheme, nUsers)
    except ValueError:
        assert True
    else:
        assert False, "Expected ValueError for invalid modulation scheme"