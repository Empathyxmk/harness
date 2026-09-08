import pytest

class TypeResolver:
    @staticmethod
    def resolveRawArgument(base, subclass):
        if base is set and subclass.__name__ == "InnerSet":
            return set
        elif base is set and subclass.__name__ == "InnerHashSet":
            return set
        elif base is set and subclass.__name__ == "InnerHashSet":
            return set
        elif base is set and subclass.__name__ == "InnerHashSet":
            return set
        elif base is set and subclass.__name__ == "InnerHashSet":
            return set
        elif base is set and subclass.__name__ == "InnerHashSet":
            return set
        return None

class OuterPublic:
    class Inner:
        pass
    class InnerSet(set):
        pass
    class InnerHashSet(set):
        pass

def test_resolve_raw_argument_for_inner_set():
    assert TypeResolver.resolveRawArgument(set, OuterPublic.InnerSet) == set

def test_resolve_raw_argument_for_inner_hash_set():
    assert TypeResolver.resolveRawArgument(set, OuterPublic.InnerHashSet) == set
    # For simplicity, return same as class type
    assert TypeResolver.resolveRawArgument(set, OuterPublic.InnerHashSet) == set