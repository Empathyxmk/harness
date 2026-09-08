package public_tests

import (
	"reflect"
	"testing"
)

type DummyMultiDex struct{}

func newDummyMultiDex() *DummyMultiDex {
	return &DummyMultiDex{}
}

func TestPrivateConstructorCoveragePublic(t *testing.T) {
	_ = newDummyMultiDex()
	// Only for code coverage -- constructor always works in Go.
}

func TestIsVMMultidexCapableEdgeCasesPublic(t *testing.T) {
	if isVMMultidexCapable(" ") {
		t.Error("Expected \" \" to be false.")
	}
	if isVMMultidexCapable("xyz") {
		t.Error("Expected \"xyz\" to be false.")
	}
	if !isVMMultidexCapable("4.2.1") {
		t.Error("Expected \"4.2.1\" to be true.")
	}
}