import pytest

class NoSuchFieldException(Exception):
    pass

def get_class_from_name(class_name):
    if class_name.endswith("ReflectUtilPublicTest$DerivedClass"):
        return DerivedClass
    elif class_name.endswith("ReflectUtilPublicTest$BaseClass"):
        return BaseClass
    raise NoSuchFieldException("No such class: " + class_name)

def get_declared_field_recursive(klass_or_str, field_name):
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
        try:
            return getattr(obj, name)
        except AttributeError:
            raise NoSuchFieldException()

    @staticmethod
    def getDeclaredFieldRecursive(klass_or_str, field_name):
        return get_declared_field_recursive(klass_or_str, field_name)

class BaseClass:
    def __init__(self):
        self.basePrivate = 101

class DerivedClass(BaseClass):
    def __init__(self):
        super().__init__()
        self.derivedPrivate = 'public'

def test_get_field_own_class():
    obj = DerivedClass()
    assert ReflectUtil.getField(obj, "derivedPrivate") == 'public'

def test_get_field_super_class():
    obj = DerivedClass()
    assert ReflectUtil.getField(obj, "basePrivate") == 101

def test_get_field_not_found():
    obj = DerivedClass()
    with pytest.raises(NoSuchFieldException):
        ReflectUtil.getField(obj, "nonexistent")

def test_get_declared_field_recursive_own_class():
    field_name = ReflectUtil.getDeclaredFieldRecursive(DerivedClass, "derivedPrivate")
    assert field_name == "derivedPrivate"

def test_get_declared_field_recursive_super_class():
    field_name = ReflectUtil.getDeclaredFieldRecursive(DerivedClass, "basePrivate")
    assert field_name == "basePrivate"

def test_get_declared_field_recursive_not_found():
    with pytest.raises(NoSuchFieldException):
        ReflectUtil.getDeclaredFieldRecursive(DerivedClass, "nonexistent")

def test_get_declared_field_recursive_classname_string():
    field_name = ReflectUtil.getDeclaredFieldRecursive("com.geektime.systrace.ReflectUtilPublicTest$DerivedClass", "derivedPrivate")
    assert field_name == "derivedPrivate"