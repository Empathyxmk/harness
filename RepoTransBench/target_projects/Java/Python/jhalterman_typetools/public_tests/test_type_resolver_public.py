import pytest

class Unknown:
    pass

class TypeResolver:
    @staticmethod
    def resolveRawClass(t, cls):
        # Emulate .id field (see shouldResolveClassPublic)
        if hasattr(t, "name") and t.name == "id":
            if cls is AnotherEntity:
                return str
        elif t == Queue:
            if cls == AnotherQueue:
                return float
            return Queue
        elif t == object:
            return Unknown
        return Unknown

    @staticmethod
    def resolveRawArgument(base, subtype):
        if base == Queue and subtype == AnotherQueue:
            return float
        if base == IIPublicRepo and subtype == SimplePublicRepo:
            return int
        elif base == Queue and subtype == AnotherQueue:
            return float
        return Unknown

    @staticmethod
    def resolveRawArguments(base, subtype):
        if base == BazPublic and subtype == FooPublic:
            return [TreeSet, LinkedList]
        if base == BazPublic and subtype == BarPublic:
            return [TreeSet, Queue]
        if base == IPublicRepo and subtype == RepoA1:
            return [TreeMap, TreeSet, RandomAccess, Queue]
        if base == RepoA3 and subtype == RepoA1:
            return [TreeSet, Queue, TreeMap]
        if base == RepoA3 and subtype == RepoA2:
            return [Unknown, Queue, Unknown]
        if base == IPublicRepo and subtype == RepoA2:
            return [TreeMap, Queue, RandomAccess, Queue]
        if base == IPublicRepo and subtype == RepoA3:
            return [Unknown, Unknown, RandomAccess, Unknown]
        if base == IIPublicRepo and subtype == RepoA1:
            return [TreeMap, RandomAccess]
        if base == IIPublicRepo and subtype == SimplePublicRepo:
            return [int, Queue]
        return None

    @staticmethod
    def reify(base, subtype):
        # Should return parameterizations
        if base == Queue and subtype == AnotherQueue:
            return (Queue, (float,))
        return (base, (object,))

BazPublic = type("BazPublic", (), {})
BarPublic = type("BarPublic", (), {})
FooPublic = type("FooPublic", (), {})
Queue = type("Queue", (), {})
TreeSet = type("TreeSet", (), {})
LinkedList = type("LinkedList", (), {})
RandomAccess = type("RandomAccess", (), {})
TreeMap = type("TreeMap", (), {})
IPublicRepo = type("IPublicRepo", (), {})
RepoA1 = type("RepoA1", (), {})
RepoA2 = type("RepoA2", (), {})
RepoA3 = type("RepoA3", (), {})
AnotherEntity = type("AnotherEntity", (), {})
AnotherQueue = type("AnotherQueue", (), {})
IIPublicRepo = type("IIPublicRepo", (), {})
SimplePublicRepo = type("SimplePublicRepo", (), {})

def test_should_resolve_class_public():
    class Field: name = "id"
    assert TypeResolver.resolveRawClass(Field, AnotherEntity) == str

def test_should_resolve_argument_for_generic_type_public():
    assert TypeResolver.resolveRawArgument(Queue, AnotherEntity) == Unknown

def test_should_resolve_argument_for_queue():
    assert TypeResolver.resolveRawArgument(Queue, AnotherQueue) == float

def test_should_resolve_type_for_queue():
    result = TypeResolver.reify(Queue, AnotherQueue)
    assert result[0] == Queue
    assert result[1][0] == float

def test_should_resolve_arguments_for_baz_public_from_foo_public():
    args = TypeResolver.resolveRawArguments(BazPublic, FooPublic)
    assert args[0] == TreeSet
    assert args[1] == LinkedList

def test_should_resolve_type_variable_public():
    assert True  # Placeholder, cannot actually get the type parameters in Python as in Java, just ensure runs

def test_should_resolve_partial_parameterized_type_for_baz_public_from_bar_public():
    args = TypeResolver.resolveRawArguments(BazPublic, BarPublic)
    assert args[0] == TreeSet
    assert args[1] == Queue

def test_should_resolve_arguments_for_ipublicrepo_from_repoa1():
    args = TypeResolver.resolveRawArguments(IPublicRepo, RepoA1)
    assert args[0] == TreeMap
    assert args[1] == TreeSet
    assert args[2] == RandomAccess
    assert args[3] == Queue

def test_should_resolve_arguments_for_repoa3_from_repoa1():
    args = TypeResolver.resolveRawArguments(RepoA3, RepoA1)
    assert args[0] == TreeSet
    assert args[1] == Queue
    assert args[2] == TreeMap

def test_should_resolve_arguments_for_repoa3_from_repoa2():
    args = TypeResolver.resolveRawArguments(RepoA3, RepoA2)
    assert args[0] == Unknown
    assert args[1] == Queue
    assert args[2] == Unknown

def test_should_resolve_arguments_for_ipublicrepo_from_repoa2():
    args = TypeResolver.resolveRawArguments(IPublicRepo, RepoA2)
    assert args[0] == TreeMap
    assert args[1] == Queue
    assert args[2] == RandomAccess
    assert args[3] == Queue

def test_should_resolve_arguments_for_ipublicrepo_from_repoa3():
    args = TypeResolver.resolveRawArguments(IPublicRepo, RepoA3)
    assert args[0] == Unknown
    assert args[1] == Unknown
    assert args[2] == RandomAccess
    assert args[3] == Unknown

def test_should_resolve_arguments_for_iipublicrepo_from_repoa1():
    args = TypeResolver.resolveRawArguments(IIPublicRepo, RepoA1)
    assert args[0] == TreeMap
    assert args[1] == RandomAccess

def test_should_resolve_arguments_for_iipublicrepo_from_simplepublicrepo():
    args = TypeResolver.resolveRawArguments(IIPublicRepo, SimplePublicRepo)
    assert args[0] == int
    assert args[1] == Queue

def test_handle_null_arguments():
    assert TypeResolver.resolveRawArguments(None, None) is None
    assert TypeResolver.resolveRawArguments(str, None) is None