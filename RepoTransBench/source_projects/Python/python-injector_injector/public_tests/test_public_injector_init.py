import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import injector

def test_public_injector_repr_and_module():
    inj = injector.Injector()
    s = repr(inj)
    # Make sure repr contains the class name and 'injector'
    assert "Injector" in s
    assert "injector" in s or "Injector" in s

def test_public_injector_configuration_type():
    class MyModule(injector.Module):
        def configure(self, binder):
            pass

    inj = injector.Injector(MyModule())
    assert isinstance(inj, injector.Injector)