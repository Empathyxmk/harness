import os
import pytest
from src.frida_detection.detection import is_frida_present, test_edge_cases

def write_fake_ps(content):
    """Helper to set up the /tmp/fake_ps.txt file for tests."""
    file_path = "/tmp/fake_ps.txt"
    with open(file_path, "w") as f:
        f.write(content)

@pytest.fixture(autouse=True)
def teardown_fake_ps_file():
    """Fixture to clean up the fake_ps.txt file after each test function."""
    file_path = "/tmp/fake_ps.txt"
    yield  # Run the test
    if os.path.exists(file_path):
        os.remove(file_path)

def test_is_frida_present_found():
    write_fake_ps("pid1 bash\npid2 frida-server\npid3 otherproc\n")
    res = is_frida_present()
    assert res == 1

def test_is_frida_present_notfound():
    write_fake_ps("pid1 bash\npid3 otherproc\n")
    res = is_frida_present()
    assert res == 0

def test_is_frida_present_error():
    # Ensure file does not exist before test
    file_path = "/tmp/fake_ps.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    res = is_frida_present()
    assert res == -1

def test_edge_cases_original():
    assert test_edge_cases(-42) == -1
    assert test_edge_cases(0) == 0
    assert test_edge_cases(1) == 2
    assert test_edge_cases(17) == 1