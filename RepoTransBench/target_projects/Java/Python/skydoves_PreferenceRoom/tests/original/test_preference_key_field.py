import pytest
from unittest.mock import Mock

class IllegalAccessException(Exception):
    pass

class PreferenceKeyField:
    def __init__(self, element, element_utils):
        self.element = element
        self.element_utils = element_utils
        self.typeStringName = None
        self.keyName = None
        self.clazzName = None

        # Simulate annotations and modifiers
        key_name_ann = element.getAnnotation('KeyName')
        typ = element.asType()
        name = element.getSimpleName()
        const_val = element.getConstantValue()
        modifiers = element.getModifiers()

        if 'PRIVATE' in modifiers:
            raise IllegalAccessException()
        if 'FINAL' not in modifiers:
            raise IllegalAccessException()
        if key_name_ann:
            self.keyName = key_name_ann.value()
        else:
            # follows capitalization logic
            self.keyName = "".join([name[0].upper()]+[c for c in name[1:]])
        self.clazzName = name
        # Very basic type checking, map to string names
        if typ == 'BOOLEAN':
            self.typeStringName = "Boolean"
        elif typ == 'String':
            self.typeStringName = "String"
        else:
            self.typeStringName = str(typ)

def make_name(n):
    return n

def test_boolean_field():
    element = Mock()
    element.getAnnotation.return_value = None
    element.asType.return_value = "BOOLEAN"
    element.getSimpleName.return_value = "flag"
    element.getConstantValue.return_value = True
    element.getModifiers.return_value = {"FINAL"}

    field = PreferenceKeyField(element, Mock())
    assert field.typeStringName == "Boolean"
    assert field.keyName == "Flag"
    assert field.clazzName == "flag"

def test_string_field_with_custom_key_name():
    key_name_annotation = Mock()
    key_name_annotation.value.return_value = "customKey"
    element = Mock()
    element.getAnnotation.return_value = key_name_annotation
    element.asType.return_value = "String"
    element.getSimpleName.return_value = "username"
    element.getConstantValue.return_value = "admin"
    element.getModifiers.return_value = {"FINAL"}

    field = PreferenceKeyField(element, Mock())
    assert field.keyName == "customKey"
    assert field.typeStringName == "String"

def test_private_field_throws():
    element = Mock()
    element.getAnnotation.return_value = None
    element.asType.return_value = "BOOLEAN"
    element.getSimpleName.return_value = "flag"
    element.getModifiers.return_value = {"PRIVATE"}
    element.getConstantValue.return_value = True
    with pytest.raises(IllegalAccessException):
        PreferenceKeyField(element, Mock())

def test_non_final_field_throws():
    element = Mock()
    element.getAnnotation.return_value = None
    element.asType.return_value = "BOOLEAN"
    element.getSimpleName.return_value = "flag"
    element.getModifiers.return_value = set()
    element.getConstantValue.return_value = True
    with pytest.raises(IllegalAccessException):
        PreferenceKeyField(element, Mock())