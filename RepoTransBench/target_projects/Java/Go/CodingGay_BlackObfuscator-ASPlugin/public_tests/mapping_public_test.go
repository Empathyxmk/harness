package public_tests

import (
	"testing"
)

// Dummy Mapping object for public test logic
type Mapping struct {
	classMappings  map[string]string
	methodMappings map[string]map[string]string
	fieldMappings  map[string]map[string]string
}

func NewMapping() *Mapping {
	return &Mapping{
		classMappings:  make(map[string]string),
		methodMappings: make(map[string]map[string]string),
		fieldMappings:  make(map[string]map[string]string),
	}
}

func (m *Mapping) putClassMapping(className, obfClassName string) {
	m.classMappings[className] = obfClassName
}
func (m *Mapping) getObfuscatedClassName(className string) string {
	return m.classMappings[className]
}
func (m *Mapping) putMethodMapping(className, methodName, obfMethodName string) {
	if m.methodMappings[className] == nil {
		m.methodMappings[className] = make(map[string]string)
	}
	m.methodMappings[className][methodName] = obfMethodName
}
func (m *Mapping) getObfuscatedMethodName(className, methodName string) string {
	if m.methodMappings[className] == nil {
		return ""
	}
	return m.methodMappings[className][methodName]
}
func (m *Mapping) putFieldMapping(className, fieldName, obfFieldName string) {
	if m.fieldMappings[className] == nil {
		m.fieldMappings[className] = make(map[string]string)
	}
	m.fieldMappings[className][fieldName] = obfFieldName
}
func (m *Mapping) getObfuscatedFieldName(className, fieldName string) string {
	if m.fieldMappings[className] == nil {
		return ""
	}
	return m.fieldMappings[className][fieldName]
}
func (m *Mapping) getClassMapping() map[string]string {
	return m.classMappings
}

func TestPutAndGetDifferentData(t *testing.T) {
	mapping := NewMapping()
	className := "top.example2024.NewClass"
	obfClassName := "aBcD_PUBLIC"
	mapping.putClassMapping(className, obfClassName)
	if mapping.getObfuscatedClassName(className) != obfClassName {
		t.Errorf("expected %q, got %q", obfClassName, mapping.getObfuscatedClassName(className))
	}

	methodName := "publicMethod2024()V"
	obfMethodName := "m2024"
	mapping.putMethodMapping(className, methodName, obfMethodName)
	if mapping.getObfuscatedMethodName(className, methodName) != obfMethodName {
		t.Errorf("expected %q, got %q", obfMethodName, mapping.getObfuscatedMethodName(className, methodName))
	}

	fieldName := "publicField2024"
	obfFieldName := "f2024"
	mapping.putFieldMapping(className, fieldName, obfFieldName)
	if mapping.getObfuscatedFieldName(className, fieldName) != obfFieldName {
		t.Errorf("expected %q, got %q", obfFieldName, mapping.getObfuscatedFieldName(className, fieldName))
	}
}

func TestToMapDifferentData(t *testing.T) {
	mapping := NewMapping()
	mapping.putClassMapping("ClassA2024", "XxYyZz")
	classMap := mapping.getClassMapping()
	if classMap["ClassA2024"] != "XxYyZz" {
		t.Errorf(`expected "XxYyZz" for "ClassA2024", got %v`, classMap["ClassA2024"])
	}
	if _, ok := classMap["ClassA2024"]; !ok {
		t.Error(`expected classMap to contain key "ClassA2024"`)
	}
}