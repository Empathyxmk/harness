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
            self.keyName = "".join([name[0].upper()]+[c for c in name[1:]])
        self.clazzName = name
        if typ == 'BOOLEAN':
            self.typeStringName = "Boolean"
        elif typ == 'String':
            self.typeStringName = "String"
        else:
            self.typeStringName = str(typ)

def test_different_boolean_field():
    element = Mock()
    element.getAnnotation.return_value = None
    element.asType.return_value = "BOOLEAN"
    element.getSimpleName.return_value = "isActive"
    element.getConstantValue.return_value = False
    element.getModifiers.return_value = {"FINAL"}
    field = PreferenceKeyField(element, Mock())
    assert field.typeStringName == "Boolean"
    assert field.keyName == "IsActive"
    assert field.clazzName == "isActive"

def test_string_field_with_another_custom_key_name():
    key_name_annotation = Mock()
    key_name_annotation.value.return_value = "anotherCustomKey"
    element = Mock()
    element.getAnnotation.return_value = key_name_annotation
    element.asType.return_value = "String"
    element.getSimpleName.return_value = "displayName"
    element.getConstantValue.return_value = "public_admin"
    element.getModifiers.return_value = {"FINAL"}
    field = PreferenceKeyField(element, Mock())
    assert field.keyName == "anotherCustomKey"
    assert field.typeStringName == "String"

def test_private_field_throws_public():
    element = Mock()
    element.getAnnotation.return_value = None
    element.asType.return_value = "BOOLEAN"
    element.getSimpleName.return_value = "isActive"
    element.getModifiers.return_value = {"PRIVATE"}
    element.getConstantValue.return_value = False
    with pytest.raises(IllegalAccessException):
        PreferenceKeyField(element, Mock())

def test_non_final_field_throws_public():
    element = Mock()
    element.getAnnotation.return_value = None
    element.asType.return_value = "BOOLEAN"
    element.getSimpleName.return_value = "isActive"
    element.getModifiers.return_value = set()
    element.getConstantValue.return_value = False
    with pytest.raises(IllegalAccessException):
        PreferenceKeyField(element, Mock())