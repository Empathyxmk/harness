import subprocess

def test_mini_runner_rcnn_helpers():
    # This test mimics running all the test_rcnn_helpers suite, here via pytest
    import pytest
    result = pytest.main(['tests/original/test_rcnn_helpers.py'])
    assert result == 0, "Some tests failed in test_rcnn_helpers"