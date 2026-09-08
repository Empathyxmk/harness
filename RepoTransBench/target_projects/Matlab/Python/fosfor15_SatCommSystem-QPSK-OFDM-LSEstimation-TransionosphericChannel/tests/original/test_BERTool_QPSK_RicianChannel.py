import pytest
import sys
import os

def test_basic_functionality():
    """
    Test that the BERTool_QPSK_RicianChannel script runs without error.
    This test attempts to import and call the main function (if any), or execute the script (if only a script).
    """
    main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    if main_dir not in sys.path:
        sys.path.insert(0, main_dir)
    try:
        try:
            from BERTool_QPSK_RicianChannel import BERTool_QPSK_RicianChannel
            BERTool_QPSK_RicianChannel()
        except ImportError:
            script_file = os.path.join(main_dir, "BERTool_QPSK_RicianChannel.py")
            if not os.path.isfile(script_file):
                pytest.skip("BERTool_QPSK_RicianChannel module or script not found. Skipping.")
            exec(open(script_file).read(), {})
        assert True, "BERTool_QPSK_RicianChannel script executed without critical errors."
    except Exception as e:
        pytest.fail(f"Script execution failed with error: {e}")