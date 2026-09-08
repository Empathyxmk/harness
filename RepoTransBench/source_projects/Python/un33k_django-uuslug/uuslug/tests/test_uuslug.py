import pytest
from unittest.mock import MagicMock, patch
from uuslug.uuslug import slugify, uuslug

class DummyField:
    def __init__(self, max_length=50):
        self.max_length = max_length

class DummyMeta:
    def get_field(self, name):
        return DummyField(max_length=13)

class DummyObjects:
    def __init__(self):
        self.slugs_taken = set()
        self.pk_excluded = None
    def all(self):
        return self
    def filter(self, **kwargs):
        d = DummyObjects()
        d.slugs_taken = self.slugs_taken.copy()
        d.pk_excluded = self.pk_excluded
        return d
    def exclude(self, pk=None):
        d = DummyObjects()
        d.slugs_taken = self.slugs_taken.copy()
        d.pk_excluded = pk
        return d
    def exists(self):
        # Simulate that if a slug we want exists in slugs_taken, return True
        # Otherwise, False
        if hasattr(self, "to_check"):
            return self.to_check in self.slugs_taken
        return False
    def filter_slug(self, slug_value):
        d = DummyObjects()
        d.slugs_taken = self.slugs_taken.copy()
        d.to_check = slug_value
        return d

class DummyInstance:
    class_obj = None
    def __init__(self, pk=None, slugs_taken=None):
        self.pk = pk
        self._meta = DummyMeta()
        self.__class__.objects = DummyObjects()
        if slugs_taken:
            self.__class__.objects.slugs_taken = set(slugs_taken)
    # For ModelBase type check
    __name__ = 'Dummy'

def test_slugify_basic():
    text = "Hello, world!"
    s = slugify(text)
    assert isinstance(s, str)
    assert s.startswith("hello-world")

def test_slugify_edge_cases():
    s = slugify("")
    assert s == ""
    s = slugify("!", separator="_")
    assert s == ""
    s = slugify("æøåü", entities=False)
    assert isinstance(s, str)

def test_uuslug_unique_slug(monkeypatch):
    instance = DummyInstance(pk=1)
    # Provide two slugs already taken, test that uuslug finds the next available.
    taken = {"hello-world", "hello-world-1"}
    instance.__class__.objects.slugs_taken = taken

    # Patch filter(**{slug_field: new_slug}).exists()
    def filter_side(**kwargs):
        v = kwargs.get('slug')
        _obj = DummyObjects()
        _obj.slugs_taken = taken
        _obj.to_check = v
        return _obj
    instance.__class__.objects.filter = filter_side
    instance.__class__.objects.exclude = lambda pk=None: instance.__class__.objects

    slug = uuslug("Hello world", instance)
    assert slug == "hello-world-2"

def test_uuslug_respects_max_length(monkeypatch):
    # Check that max_length (from model field) is respected
    instance = DummyInstance()
    instance._meta = DummyMeta()
    # Patch filter to always say exists for vanilla slug, so it triggers length limiting
    taken = {"a-very-long-sl", "a-very-long-sl-1"}
    instance.__class__.objects.slugs_taken = taken
    def filter_side(**kwargs):
        v = kwargs.get('slug')
        _obj = DummyObjects()
        _obj.slugs_taken = taken
        _obj.to_check = v
        return _obj
    instance.__class__.objects.filter = filter_side
    instance.__class__.objects.exclude = lambda pk=None: instance.__class__.objects

    slug = uuslug("A very long slug", instance)
    assert "a-very-long" in slug

def test_uuslug_filter_dict(monkeypatch):
    instance = DummyInstance()
    dummy_objects = DummyObjects()
    called = {}
    def filter_dict_func(**kwargs):
        called.update(kwargs)
        return dummy_objects
    instance.__class__.objects.filter = filter_dict_func
    instance.__class__.objects.exclude = lambda pk=None: instance.__class__.objects

    uuslug("test", instance, filter_dict={'author': 'x'})
    assert "author" in called

def test_uuslug_with_pk(monkeypatch):
    instance = DummyInstance(pk=5)
    dummy_objects = DummyObjects()
    def exclude_func(pk=None):
        assert pk == 5
        return dummy_objects
    instance.__class__.objects.filter = lambda **kwargs: dummy_objects
    instance.__class__.objects.exclude = exclude_func

    uuslug("test", instance)

def test_uuslug_modelbase_exception():
    from django.db.models.base import ModelBase
    class DummyModel(metaclass=ModelBase): pass
    model_instance = DummyModel
    with pytest.raises(Exception) as e:
        uuslug("test", model_instance)
    assert "you must pass an instance" in str(e.value)