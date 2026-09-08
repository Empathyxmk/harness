import pytest

@pytest.mark.skip(reason="Skipping test_compiler due to dependency on external thrift compiler/tools")
def test_dummy_compiler():
    assert True