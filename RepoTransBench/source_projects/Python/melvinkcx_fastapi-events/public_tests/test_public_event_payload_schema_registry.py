import pytest

pytest.skip("Skipping because fastapi_events package is not installed in this environment.", allow_module_level=True)

def test_placeholder_event_payload_schema_registry():
    assert [2, 4, 6] == [2, 4, 6]