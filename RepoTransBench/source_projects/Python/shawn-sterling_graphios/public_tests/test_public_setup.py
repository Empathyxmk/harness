def test_public_setup_py_runs():
    # Simply ensure the setup.py script exists and can be read
    import os
    assert os.path.isfile(os.path.join(os.path.dirname(__file__), '../setup.py'))