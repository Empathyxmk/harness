import pytest
import uuslug.uuslug as uuslug_mod

def test_uuslug_raises_for_model_base():
    # Fix: The function is accessible as uuslug_mod.uuslug, passing a non-instance
    with pytest.raises(Exception):
        uuslug_mod.uuslug("abc", object())