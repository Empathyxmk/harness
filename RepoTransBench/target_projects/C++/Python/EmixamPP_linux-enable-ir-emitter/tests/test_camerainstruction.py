import pytest

@pytest.mark.skip(reason="Skipping tests due to lack of <format> header support on this compiler.")
def test_disabled_due_to_format():
    pass  # Skipped test, placeholder body is required for pytest but marked as skipped