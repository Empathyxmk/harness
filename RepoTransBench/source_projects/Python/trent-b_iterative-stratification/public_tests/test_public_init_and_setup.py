import os
import importlib.util

def test_public_readme_exists():
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "..", "README.md"))

def test_public_license_exists():
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "..", "LICENSE"))

def test_public_import_iterstrat():
    import iterstrat
    assert iterstrat is not None

def test_public_import_ml_stratifiers():
    from iterstrat import ml_stratifiers
    # Choose another class or function to check for in public test
    assert hasattr(ml_stratifiers, 'MultilabelStratifiedShuffleSplit')