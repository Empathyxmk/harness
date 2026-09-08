import os
import importlib.util

def test_readme_exists():
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "..", "README.md"))

def test_license_exists():
    assert os.path.exists(os.path.join(os.path.dirname(__file__), "..", "LICENSE"))

def test_import_iterstrat():
    # Check iterstrat is a package and can be imported
    import iterstrat
    assert iterstrat is not None

def test_import_ml_stratifiers():
    # Direct import of ml_stratifiers for coverage
    from iterstrat import ml_stratifiers
    assert hasattr(ml_stratifiers, 'MultilabelStratifiedKFold')

# Remove the setup.py functional test as it triggers setuptools when run outside CLI