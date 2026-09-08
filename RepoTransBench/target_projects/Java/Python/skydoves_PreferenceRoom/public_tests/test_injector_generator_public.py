import pytest
from unittest.mock import Mock

class TypeSpec:
    def __init__(self, name, body):
        self.name = name
        self.body = body
    def __str__(self):
        return self.body

class InjectorGenerator:
    def __init__(self, pcac, injected_element, element_utils):
        self.pcac = pcac
        self.injected_element = injected_element
        self.element_utils = element_utils
    def generate(self):
        name = f"{self.injected_element.getSimpleName()}_Injector"
        body = f"class {name} uses PreferenceRoom"
        return TypeSpec(name, body)

def test_generate_different_class_name():
    pcac = Mock()
    injected_element = Mock()
    element_utils = Mock()
    injected_element.getSimpleName.return_value = "PublicClass"
    element_utils.getPackageOf.return_value = Mock()
    generator = InjectorGenerator(pcac, injected_element, element_utils)
    spec = generator.generate()
    assert spec.name == "PublicClass_Injector"
    assert "PreferenceRoom" in str(spec)