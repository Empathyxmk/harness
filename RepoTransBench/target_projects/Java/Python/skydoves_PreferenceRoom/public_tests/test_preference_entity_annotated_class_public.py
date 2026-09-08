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

def test_missing_entity_name_throws_public():
    type_element = Mock()
    elements = Mock()
    annotation = Mock()
    type_element.getAnnotation.return_value = annotation
    annotation.value.return_value = ""
    type_element.getSimpleName.return_value = "TestPreference"
    elements.getPackageOf.return_value = Mock(isUnnamed=lambda: False, getQualifiedName=lambda: "public.pkg")
    type_element.getEnclosedElements.return_value = []
    with pytest.raises(VerifyException):
        PreferenceEntityAnnotatedClass(type_element, elements)

def test_with_different_default_preference_and_encrypt_entity():
    type_element = Mock()
    elements = Mock()
    pe = Mock()
    dp = Mock()
    ee = Mock()
    type_element.getAnnotation.side_effect = lambda arg: {"PreferenceEntity": pe, "DefaultPreference": dp, "EncryptEntity": ee}.get(arg)
    type_element.getSimpleName.return_value = "NameB"
    pe.value.return_value = "EntityY"
    elements.getPackageOf.return_value = Mock()
    type_element.getEnclosedElements.return_value = []
    ee.value.return_value = "PUBLIC_ENCRYPTED_VAL"
    clz = PreferenceEntityAnnotatedClass(type_element, elements)
    assert clz.entityName == "EntityY"
    assert clz.isDefaultPreference
    assert clz.isEncryption
    assert clz.encryptionKey == "PUBLIC_ENCRYPTED_VAL"