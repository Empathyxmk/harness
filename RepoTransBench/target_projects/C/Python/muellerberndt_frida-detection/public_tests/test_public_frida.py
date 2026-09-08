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

def test_detect_frida_absent_with_other_processes():
    write_fake_ps("myapp\nsshd\nbash\nvpnclient\n")
    result = is_frida_present()
    assert result == 0

def test_detect_frida_present_amid_noise():
    write_fake_ps("procX\nprocY\nfrida-server-something\nprocZ\n")
    result = is_frida_present()
    assert result == 1

def test_detect_frida_present_exact():
    write_fake_ps("procA\nfrida-server\nprocB\n")
    result = is_frida_present()
    assert result == 1

def test_detect_frida_error_open():
    # Ensure file does not exist for this test
    file_path = "/tmp/fake_ps.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
    result = is_frida_present()
    assert result == -1

def test_edge_cases_public():
    assert test_edge_cases(-15) == -1
    assert test_edge_cases(7) == 1
    assert test_edge_cases(10) == 1
    assert test_edge_cases(0) == 0
    assert test_edge_cases(1) == 2