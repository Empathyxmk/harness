"""
Public test: Disabled due to compilation issues in private sources - alternate test name.
Remains commented for the same reason as the private test.
"""

import pytest

@pytest.mark.skip(reason="Disabled due to missing types/dependencies (as in C++ public test)")
def test_disabled_due_to_missing_types_public():
    # Always succeed if enabled, but skipped for missing dependencies.
    assert True