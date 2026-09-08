import pytest

def test_public_utils_matlab_all():
    # These run the public test_rcnn_helpers, and utils/public_test_2010_from_2012
    # Simulate that all tests in public_test_rcnn_helpers ("public_tests/test_public_test_rcnn_helpers.py")
    # are run. We rely on Pytest to do this, and test_public_test_rcnn_helpers.py
    # is automatically discovered and run by pytest.
    # Here, explicitly import and run the public util test for 2010_from_2012.
    from public_tests.test_public_test_2010_from_2012 import test_public_2010_from_2012
    test_public_2010_from_2012()