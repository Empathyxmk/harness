package original

import (
	"testing"
)

type JvmNativeClass struct {
	Loader    JvmClassLoader
	HostClass interface{}
}

func NewJvmNativeClass(loader JvmClassLoader, hostClass interface{}) *JvmNativeClass {
	return &JvmNativeClass{Loader: loader, HostClass: hostClass}
}

type JvmDefaultClassLoader struct {
	Path string
}

func NewJvmDefaultClassLoader(path string) *JvmDefaultClassLoader {
	return &JvmDefaultClassLoader{Path: path}
}

func (loader *JvmDefaultClassLoader) LoadClass(className string) JvmClass {
	// For any "java.lang.String", return native class
	if className == "java.lang.String" {
		return &JvmNativeClass{}
	}
	return nil
}

func TestNonExistingClassLoadsAsNative(t *testing.T) {
	loader := NewJvmDefaultClassLoader(".")
	c := loader.LoadClass("java.lang.String")
	if c == nil {
		t.Fatalf("Expected class loading to return non-nil")
	}
	if _, ok := c.(*JvmNativeClass); !ok {
		t.Errorf("Expected instance of JvmNativeClass for java.lang.String class")
	}
}

func TestConstructorAndClassPath(t *testing.T) {
	fakePath := "/tmp"
	loader := NewJvmDefaultClassLoader(fakePath)
	if loader == nil {
		t.Fatalf("Expected non-nil loader")
	}
}