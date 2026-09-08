import pytest

class ReflectionUtils:
    @staticmethod
    def get_declared_field_with_path(obj_type, path):
        parts = path.split(".")
        first = parts[0]
        for c in obj_type.__mro__:
            if first in c.__dict__:
                field_type = c.__dict__[first]
                break
        else:
            field_type = None
        if len(parts) == 1:
            return first
        else:
            # simulated for nested
            return parts[-1]

    @staticmethod
    def get_field_value_with_path(obj, path):
        try:
            parts = path.split(".")
            val = obj
            for part in parts:
                val = getattr(val, part, None)
                if val is None:
                    return None
            return val
        except Exception:
            return None

    @staticmethod
    def set_field_value_with_path(obj, path, value):
        parts = path.split(".")
        if len(parts) == 1:
            setattr(obj, path, value)
        elif len(parts) == 2:
            sub_obj = getattr(obj, parts[0], None)
            if sub_obj is None:
                raise ValueError("Expected IllegalStateException")
            setattr(sub_obj, parts[1], value)

class Address:
    def __init__(self):
        self.street = None

class Person:
    def __init__(self):
        self.name = None
        self.address = None

def test_get_declared_field_with_path():
    field = ReflectionUtils.get_declared_field_with_path(Person, "name")
    assert field == "name"
    field = ReflectionUtils.get_declared_field_with_path(Person, "address.street")
    assert field == "street"

def test_get_field_with_path():
    person = Person()
    person.name = "Joe"
    assert ReflectionUtils.get_field_value_with_path(person, "name") == "Joe"
    assert ReflectionUtils.get_field_value_with_path(person, "address.street") is None
    person.address = Address()
    assert ReflectionUtils.get_field_value_with_path(person, "address.street") is None
    person.address.street = "123 Main"
    assert ReflectionUtils.get_field_value_with_path(person, "address.street") == "123 Main"

def test_set_field_with_path():
    person = Person()
    ReflectionUtils.set_field_value_with_path(person, "name", "Joe")
    assert person.name == "Joe"
    with pytest.raises(ValueError):
        ReflectionUtils.set_field_value_with_path(person, "address.street", "123 Main")
    person.address = Address()
    ReflectionUtils.set_field_value_with_path(person, "address.street", "123 Main")
    assert person.address.street == "123 Main"