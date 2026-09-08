import pytest

@pytest.mark.skip(reason="requires 'hg' executable and real VCS setup, skipping in CI")
def test_cli_placeholder():
    pass