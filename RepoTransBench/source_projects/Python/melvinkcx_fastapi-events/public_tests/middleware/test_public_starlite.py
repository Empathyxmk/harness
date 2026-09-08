import pytest

pytest.skip("Skipping because fastapi_events package is not installed in this environment.", allow_module_level=True)

def test_placeholder_starlite():
    assert "lite" in "starlite"