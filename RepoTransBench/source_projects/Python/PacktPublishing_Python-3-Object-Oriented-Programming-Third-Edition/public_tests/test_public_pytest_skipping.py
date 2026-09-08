import sys
import pytest

def test_simple_skip_public():
    # Use a different platform to trigger skip
    if sys.platform != "another_fakeos":
        pytest.skip("Test works only on another_fakeOS")

    # these lines should not be executed in any real env
    assert False, "Should not reach here"

@pytest.mark.skipif("sys.version_info < (3,8)")
def test_python38_public():
    # Only run on Python >=3.8: new test but compatible logic
    assert int("42") == 42