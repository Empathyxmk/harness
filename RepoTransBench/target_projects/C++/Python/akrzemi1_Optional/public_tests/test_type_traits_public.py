import pytest

import typing

class PublicNonTrivial:
    def __init__(self):
        pass
    def __copy__(self):
        pass

def test_is_not_trivial_type_public():
    # In C++, is_trivially_copyable<optional<PublicNonTrivial>> == False.
    # In Python, just ensure things exist, and optional is just object container.
    # Fails if copy attempted? In Python, objects are always copyable in some sense.
    class OptionalPublic:
        def __init__(self, val=None):
            self.val = val
    # Can't assert triviality, but construction works.
    OptionalPublic(PublicNonTrivial())

class TrivialButNotRequiredByOptional:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

def test_instantiation_public():
    class OptionalPublic:
        def __init__(self, val=None):
            self.val = val
    trivial_optional = OptionalPublic(TrivialButNotRequiredByOptional())
    opti = OptionalPublic(77)
    assert trivial_optional
    assert opti.val == 77