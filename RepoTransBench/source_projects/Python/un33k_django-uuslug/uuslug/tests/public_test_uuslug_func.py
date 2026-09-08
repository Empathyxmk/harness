import pytest
import uuslug.uuslug as uuslug_mod

def test_uuslug_raises_for_model_base_public():
    class Dummy:
        pass
    # Use a different type as the instance
    with pytest.raises(Exception):
        uuslug_mod.uuslug("def", Dummy())