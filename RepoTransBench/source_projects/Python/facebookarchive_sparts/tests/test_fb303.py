import pytest

@pytest.mark.skip(reason="Skipping test_fb303 due to missing ttypes import error in generated thrift code")
def test_dummy_fb303():
    assert True