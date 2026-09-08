import pytest
from unittest.mock import Mock

class VerifyException(Exception):
    pass

class PreferenceEntityAnnotatedClass:
    def __init__(self, type_element, elements):
        annotation = type_element.getAnnotation('PreferenceEntity')
        if annotation is None or annotation.value() == "":
            raise VerifyException()
        self.entityName = annotation.value()
        self.isDefaultPreference = type_element.getAnnotation('DefaultPreference') is not None
        encrypt_annotation = type_element.getAnnotation('EncryptEntity')
        self.isEncryption = encrypt_annotation is not None
        self.encryptionKey = encrypt_annotation.value() if encrypt_annotation else None

def test_missing_entity_name_throws():
    type_element = Mock()
    elements = Mock()
    annotation = Mock()
    type_element.getAnnotation.return_value = annotation
    annotation.value.return_value = ""
    type_element.getSimpleName.return_value = "MyPreference"
    elements.getPackageOf.return_value = Mock(isUnnamed=lambda: False, getQualifiedName=lambda: "pkg")
    type_element.getEnclosedElements.return_value = []
    with pytest.raises(VerifyException):
        PreferenceEntityAnnotatedClass(type_element, elements)

def test_with_default_preference_and_encrypt_entity():
    type_element = Mock()
    elements = Mock()
    pe = Mock()
    dp = Mock()
    ee = Mock()
    type_element.getAnnotation.side_effect = lambda arg: {"PreferenceEntity": pe, "DefaultPreference": dp, "EncryptEntity": ee}.get(arg)
    type_element.getSimpleName.return_value = "NameA"
    pe.value.return_value = "EntityX"
    elements.getPackageOf.return_value = Mock()
    type_element.getEnclosedElements.return_value = []
    ee.value.return_value = "ENCRYPTED_VALUE"

    clz = PreferenceEntityAnnotatedClass(type_element, elements)
    assert clz.entityName == "EntityX"
    assert clz.isDefaultPreference
    assert clz.isEncryption
    assert clz.encryptionKey == "ENCRYPTED_VALUE"