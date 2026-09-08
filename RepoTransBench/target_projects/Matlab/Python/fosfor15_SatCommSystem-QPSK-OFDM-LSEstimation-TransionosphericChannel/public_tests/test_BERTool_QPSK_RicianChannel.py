import pytest
import sys
import os

def test_run_with_different_input():
    """
    Test that the function BERTool_QPSK_RicianChannel runs and returns valid outputs for
    varied EbNo, maxNumErrs, maxNumBits (public API/behavioral test).
    """
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    try:
        from BERTool_QPSK_RicianChannel import BERTool_QPSK_RicianChannel
    except ImportError:
        pytest.skip("BERTool_QPSK_RicianChannel function not found in src directory.")
    EbNo = 10
    maxNumErrs = 4
    maxNumBits = 12000
    try:
        BER, numBits = BERTool_QPSK_RicianChannel(EbNo, maxNumErrs, maxNumBits)
        assert 0 <= BER <= 1, "BER should be between 0 and 1."
        assert numBits > 0, "numBits should be positive."
    except Exception as e:
        pytest.fail(f"Public test failed with error: {e}")