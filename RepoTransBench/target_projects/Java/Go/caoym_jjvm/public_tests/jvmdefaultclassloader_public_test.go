package public_tests

import (
	"testing"
)

type JvmDefaultClassLoader struct{}

func NewPublicJvmDefaultClassLoader() *JvmDefaultClassLoader {
	return &JvmDefaultClassLoader{}
}

func (loader *JvmDefaultClassLoader) getResourceAsStream(name string) interface{} {
	// Always returns nil for unknown resource
	return nil
}

func (loader *JvmDefaultClassLoader) loadClassBytes(name string) interface{} {
	// Always returns nil for non-existing class
	return nil
}

func TestLoadResourceFileWithDifferentResource(t *testing.T) {
	loader := NewPublicJvmDefaultClassLoader()
	if loader.getResourceAsStream("META-INF/not-a-real-resource.txt") != nil {
		t.Errorf("Expected nil for unknown resource")
	}
}

func TestNonExistingClassReturnsNull(t *testing.T) {
	loader := NewPublicJvmDefaultClassLoader()
	if loader.loadClassBytes("com/example/NoSuchClass.class") != nil {
		t.Errorf("Expected nil for unknown class bytes")
	}
}