import pytest

class DummySuper:
    def deconstruct(self):
        return ("name", "path", (), {})

def test_shortuuidfield_deconstruct_and_generate(monkeypatch):
    # We'll test without needing Django
    from shortuuid.django_fields import ShortUUIDField
    # Monkeypatch models.CharField and translation
    monkeypatch.setattr("shortuuid.django_fields.models.CharField", DummySuper)
    monkeypatch.setattr("shortuuid.django_fields._", lambda x: x)
    # Patch shortuuid.ShortUUID to a dummy
    class DummyShortUUID:
        def __init__(self, alphabet=None, dont_sort_alphabet=False):
            pass
        def random(self, length):
            return "X"*length
    monkeypatch.setattr("shortuuid.django_fields.ShortUUID", DummyShortUUID)
    # Now create
    field = ShortUUIDField(length=5, prefix="PRE_", dont_sort_alphabet=True, alphabet="abc")
    # Should call dummy generate
    val = field._generate_uuid()
    assert val == "PRE_" + "X"*5
    # deconstruct should have expected items
    name, path, args, kwargs = field.deconstruct()
    assert kwargs["length"] == 5
    assert kwargs["prefix"] == "PRE_"
    assert kwargs["alphabet"] == "abc"
    assert "default" not in kwargs

def test_shortuuidfield_default_max_length_and_args(monkeypatch):
    from shortuuid.django_fields import ShortUUIDField
    monkeypatch.setattr("shortuuid.django_fields.models.CharField", DummySuper)
    monkeypatch.setattr("shortuuid.django_fields._", lambda x: x)
    class DummyShortUUID:
        def __init__(self, alphabet=None, dont_sort_alphabet=False):
            pass
        def random(self, length):
            return "Z"*length
    monkeypatch.setattr("shortuuid.django_fields.ShortUUID", DummyShortUUID)
    # Omit max_length, should set to length+len(prefix)
    field = ShortUUIDField(length=6, prefix="Q_", alphabet="123", dont_sort_alphabet=False)
    assert field.length == 6
    assert field.prefix == "Q_"
    assert field.alphabet == "123"
    # max_length defaults
    assert hasattr(field, 'max_length') or hasattr(field, '_max_length')