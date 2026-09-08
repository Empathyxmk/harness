import sys
import os
import pytest

# Ensure the parent directory is on sys.path, so "import injector" works for the public test.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import injector

def test_public_singleton_binding_unique_value():
    class Alpha:
        pass

    class Beta:
        pass

    inj = injector.Injector([
        injector.InstanceProvider(Alpha, Alpha()),
        injector.InstanceProvider(Beta, Beta())
    ])
    a1 = inj.get(Alpha)
    b1 = inj.get(Beta)
    assert isinstance(a1, Alpha)
    assert isinstance(b1, Beta)
    assert a1 is inj.get(Alpha)
    assert b1 is inj.get(Beta)

def test_public_inject_decorator_with_primitive():
    class Service:
        pass

    @injector.inject
    def provide(value: int = injector.Provide[int]):
        return value

    inj = injector.Injector({int: 77})
    result = inj.call_with_injection(provide)
    assert result == 77

def test_public_provider_reuse_types():
    class Foo:
        pass

    inj = injector.Injector([injector.InstanceProvider(Foo, Foo())])
    foo1 = inj.get(Foo)
    foo2 = inj.get(Foo)
    assert foo1 is foo2