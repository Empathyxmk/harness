package original

import (
	"reflect"
	"testing"
)

type dummyMultiDex struct{}

// Simulate a package-private constructor (not enforced in Go)
func newDummyMultiDex() *dummyMultiDex {
	return &dummyMultiDex{}
}

func TestPrivateConstructorCoverage(t *testing.T) {
	// In Java this is for code coverage of the private constructor, not needed in Go.
	instance := newDummyMultiDex()
	if instance == nil {
		t.Error("Expected non-nil instance.")
	}
	typ := reflect.TypeOf(instance)
	if typ.String() != "*original.dummyMultiDex" {
		t.Errorf("Constructor returned type %s, want *original.dummyMultiDex", typ.String())
	}
}

func TestIsVMMultidexCapableEdgeCases(t *testing.T) {
	if isVMMultidexCapable("") {
		t.Error("Expected \"\" to be false.")
	}
	if isVMMultidexCapable("abc.def") {
		t.Error("Expected \"abc.def\" to be false.")
	}
	if !isVMMultidexCapable("3.10.99") {
		t.Error("Expected \"3.10.99\" to be true.")
	}
}