# Test setup.py without importing it directly to avoid running setup()
# Instead, check for the file presence and its main elements as a text artifact

import os

def test_setup_py_exists_and_has_setup_call():
    assert os.path.exists("setup.py")
    with open("setup.py") as f:
        content = f.read()
    assert "setup(" in content
    assert "__name__" in content