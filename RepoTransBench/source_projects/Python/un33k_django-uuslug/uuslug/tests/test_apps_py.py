import pytest
from uuslug import apps

def test_apps_module_import():
    assert hasattr(apps, "AppConfig") or hasattr(apps, "UuslugConfig") or hasattr(apps, "__file__")

def test_apps_module_smoke():
    # Just ensure the module is importable, and has doc or meta info
    assert apps.__doc__ is None or isinstance(apps.__doc__, str)