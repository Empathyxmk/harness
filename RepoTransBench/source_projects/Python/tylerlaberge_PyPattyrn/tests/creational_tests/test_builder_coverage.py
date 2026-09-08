import pytest
from pypattyrn.creational import builder

class MyObject:
    def __init__(self):
        self.parts = []

class MyBuilder(builder.Builder):
    def __init__(self, obj):
        super().__init__(obj)
        self._register("add_part", self.build_part)

    def build_part(self, part=None):
        self.constructed_object.parts.append(part or "default")

class MyDirector(builder.Director):
    def __init__(self):
        super().__init__()
        self.builder = MyBuilder(MyObject())

    def construct(self):
        self.builder.build("add_part", part="A")
        self.builder.build("add_part", part="B")

def test_director_get_constructed_object():
    d = MyDirector()
    d.construct()
    obj = d.get_constructed_object()
    assert obj.parts == ['A', 'B']

def test_builder_build_method_registration_and_build():
    obj = MyObject()
    b = MyBuilder(obj)
    b.build("add_part", part="X")
    b.build("add_part") # Should use default
    assert obj.parts == ["X", "default"]

def test_builder_register_and_overwrite():
    obj = MyObject()
    b = MyBuilder(obj)
    called = []
    def new_builder_func(part=None):
        called.append(True)
    b._register("add_part", new_builder_func)
    b.build("add_part")
    assert called

def test_director_abstract_construct_raises():
    import abc
    # Try to instantiate a pure abstract Director without implement construct
    # This must be caught at class definition, so we skip error here:
    class DummyDir(builder.Director):
        pass
    with pytest.raises(TypeError):
        DummyDir()

def test_builder_init_sets_attrs():
    obj = MyObject()
    b = MyBuilder(obj)
    assert b.constructed_object == obj
    assert isinstance(b.build_methods, dict)