package original

import (
	"testing"
)

type KeyRepresentation string

const (
	Base32 KeyRepresentation = "BASE32"
	Base64 KeyRepresentation = "BASE64"
)

func TestKeyRepresentationValues(t *testing.T) {
	reps := []KeyRepresentation{Base32, Base64}
	if reps == nil {
		t.Fatal("Representation array is nil")
	}
	if len(reps) == 0 {
		t.Error("Expected length > 0")
	}
}

func TestKeyRepresentationValueOf(t *testing.T) {
	if Base32 != KeyRepresentation("BASE32") {
		t.Error("BASE32 value mismatch")
	}
	if Base64 != KeyRepresentation("BASE64") {
		t.Error("BASE64 value mismatch")
	}
}