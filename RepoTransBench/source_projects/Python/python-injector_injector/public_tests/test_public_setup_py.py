import os

def test_public_version_exists():
    version_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "setup.py")
    with open(version_file) as f:
        setup_py = f.read()
    assert "version" in setup_py

def test_public_description_exists():
    setup_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "setup.py")
    with open(setup_file) as f:
        setup_content = f.read()
    assert "description" in setup_content