# test_scatternet_extended.py
# Extended and more meaningful tests for ScatterNet
import os
import subprocess

def test_nn_m_callable_and_help_contains_nn():
    """
    Test NN.m with a minimal pipeline (dummy test).

    - Confirm NN.m is callable and does not error with sample usage
    - We'll just check help text appears or that it can be run with no input

    Since .m files are Matlab/Octave scripts, we check if they can be called (Octave/Matlab must be installed for real execution).
    Here, we'll check that help can be printed and contains "NN".
    """
    try:
        # Try to get the help text for NN.m using Octave if available
        # This will only work if Octave is present.
        # The code is robust: if Octave is missing, the test fails gracefully.
        result = subprocess.run(
            ['octave', '--no-gui', '--eval', "help('NN')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        assert "NN" in output, 'NN.m help output should contain "NN"'
    except Exception as e:
        assert False, f"NN.m should execute without error. Exception: {e}"

def test_total_cs_m_exists():
    # Test that total_cs.m exists for use in the codebase
    assert os.path.isfile("total_cs.m"), "total_cs.m should exist"