package public_tests

import (
	"testing"
	"strings"
)

type EmptyCollectionException struct{ msg string }
func (e EmptyCollectionException) Error() string { return e.msg }

type InvalidKeyException struct{ msg string }
func (e InvalidKeyException) Error() string { return e.msg }

type InvalidOperationException struct{ msg string }
func (e InvalidOperationException) Error() string { return e.msg }

func TestEmptyCollectionExceptionMessage(t *testing.T) {
	ex := EmptyCollectionException{"Nothing to iterate with public test!"}
	if !strings.Contains(ex.Error(), "Nothing to iterate") {
		t.Errorf("Expected specific message got %v", ex.Error())
	}
}

func TestInvalidKeyExceptionMessage(t *testing.T) {
	ex := InvalidKeyException{"Invalid KEY provided in public test."}
	if !strings.Contains(ex.Error(), "KEY provided") {
		t.Errorf("Expected 'KEY provided' message got %v", ex.Error())
	}
}

func TestInvalidOperationExceptionMessage(t *testing.T) {
	ex := InvalidOperationException{"Operation not allowed in public test."}
	if !strings.Contains(ex.Error(), "not allowed") {
		t.Errorf("Expected 'not allowed' message got %v", ex.Error())
	}
}

func TestEmptyCollectionExceptionIsInstanceOfError(t *testing.T) {
	ex := EmptyCollectionException{"Another public empty collection error."}
	if !strings.Contains(strings.ToLower(ex.Error()), "empty collection") {
		t.Errorf("Expected 'empty collection' in error message")
	}
}

func TestInvalidKeyExceptionIsInstanceOfError(t *testing.T) {
	ex := InvalidKeyException{"Trying a different invalid key in public test."}
	if !strings.Contains(strings.ToLower(ex.Error()), "invalid key") {
		t.Errorf("Expected 'invalid key' in error message: %v", ex.Error())
	}
}

func TestInvalidOperationExceptionIsInstanceOfError(t *testing.T) {
	ex := InvalidOperationException{"A variant operation error in public test."}
	if !strings.Contains(strings.ToLower(ex.Error()), "operation error") {
		t.Errorf("Expected 'operation error' in error message: %v", ex.Error())
	}
}