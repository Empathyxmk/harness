import pytest
import os

def test_script_executes():
    # Try to run the main script, should return True if no exceptions
    from src.lips.main_MAINSCRIPT import main_MAINSCRIPT
    try:
        main_MAINSCRIPT()
        pass_flag = True
    except Exception:
        pass_flag = False
    assert pass_flag