import pytest

class NoSuchFieldException(Exception):
    pass

def get_class_from_name(class_name):
    # Emulate class name resolution for test classes.
    if class_name.endswith("ReflectUtilTest$SubClass"):
        return SubClass
    elif class_name.endswith("ReflectUtilTest$SuperClass"):
        return SuperClass
    raise NoSuchFieldException("No such class: " + class_name)

def get_declared_field_recursive(klass_or_str, field_name):
    # returns the field name (string), which is then used to get/set on the instance
    if isinstance(klass_or_str, str):
        klass = get_class_from_name(klass_or_str)
    elif isinstance(klass_or_str, type):
        klass = klass_or_str
    else:
        raise ValueError("Bad type for klass")
    for c in klass.mro():
        if field_name in c.__dict__:
            return field_name
    raise NoSuchFieldException()

class ReflectUtil:
    @staticmethod
    def getField(obj, name):
        # For testing static method, just access the attribute
        try:
            return getattr(obj, name)
        except AttributeError:
            raise NoSuchFieldException()

    @staticmethod
    def getDeclaredFieldRecursive(klass_or_str, field_name):
        return get_declared_field_recursive(klass_or_str, field_name)

class SuperClass:
    def __init__(self):
        self.superPrivate = 42

class SubClass(SuperClass):
    def __init__(self):
        super().__init__()
        self.subPrivate = 'secret'

def test_get_field_own_class():
    obj = SubClass()
    assert ReflectUtil.getField(obj, "subPrivate") == 'secret'

def test_get_field_super_class():
    obj = SubClass()
    assert ReflectUtil.getField(obj, "superPrivate") == 42

def test_get_field_not_found():
    obj = SubClass()
    with pytest.raises(NoSuchFieldException):
        ReflectUtil.getField(obj, "nonexistent")

def test_get_declared_field_recursive_own_class():
    field_name = ReflectUtil.getDeclaredFieldRecursive(SubClass, "subPrivate")
    assert field_name == "subPrivate"

def test_get_declared_field_recursive_super_class():
    field_name = ReflectUtil.getDeclaredFieldRecursive(SubClass, "superPrivate")
    assert field_name == "superPrivate"

def test_get_declared_field_recursive_not_found():
    with pytest.raises(NoSuchFieldException):
        ReflectUtil.getDeclaredFieldRecursive(SubClass, "nonexistent")

def test_get_declared_field_recursive_classname_string():
    field_name = ReflectUtil.getDeclaredFieldRecursive("com.geektime.systrace.ReflectUtilTest$SubClass", "subPrivate")
    assert field_name == "subPrivate"