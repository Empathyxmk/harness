package public_tests

import (
	"testing"
	. "orcasgit_django_fernet_fields/tests"
)

func TestEncryptedFieldBasic_Public(t *testing.T) {
	value := "This is secret data for pub"
	field := NewEncryptedTextField()
	enc, err := field.GetPrepValue(value)
	if err != nil {
		t.Fatalf("Encryption failed: %v", err)
	}
	dec, err := field.FromDBValue(enc)
	if err != nil {
		t.Fatalf("Decryption failed: %v", err)
	}
	if dec != value {
		t.Errorf("Expected %q, got %q", value, dec)
	}
}

func TestEncryptedCharField_Public(t *testing.T) {
	value := "AlphaBravo"
	field := NewEncryptedCharField(32)
	enc, err := field.GetPrepValue(value)
	if err != nil {
		t.Fatalf("Encryption failed: %v", err)
	}
	dec, err := field.FromDBValue(enc)
	if err != nil {
		t.Fatalf("Decryption failed: %v", err)
	}
	if dec != value {
		t.Errorf("Expected %q, got %q", value, dec)
	}
}

func TestEncryptedFieldEmptyString_Public(t *testing.T) {
	value := ""
	field := NewEncryptedTextField()
	enc, err := field.GetPrepValue(value)
	if err != nil {
		t.Fatalf("Encryption failed: %v", err)
	}
	dec, err := field.FromDBValue(enc)
	if err != nil {
		t.Fatalf("Decryption failed: %v", err)
	}
	if dec != "" {
		t.Errorf("Expected empty string, got %q", dec)
	}
}

func TestEncryptedFieldParametrize_Public(t *testing.T) {
	testCases := []string{
		"fox jumps over the lazy dog",
		"crazy_test_value_PUBLIC_CASE",
		"another secret message",
	}
	field := NewEncryptedTextField()
	for _, val := range testCases {
		enc, err := field.GetPrepValue(val)
		if err != nil {
			t.Fatalf("Encryption failed: %v", err)
		}
		dec, err := field.FromDBValue(enc)
		if err != nil {
			t.Fatalf("Decryption failed: %v", err)
		}
		if dec != val {
			t.Errorf("Expected %q, got %q", val, dec)
		}
	}
}