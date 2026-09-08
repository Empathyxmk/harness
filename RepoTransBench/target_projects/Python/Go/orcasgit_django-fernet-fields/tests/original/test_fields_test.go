package original

import (
	"testing"
	. "orcasgit_django_fernet_fields/tests"
)

func TestEncryptedField(t *testing.T) {
	value := "Secret Data"
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

func TestEncryptedCharField(t *testing.T) {
	value := "HelloWorld"
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

func TestEncryptedFieldEmptyString(t *testing.T) {
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

func TestEncryptedFieldParametrize(t *testing.T) {
	testCases := []string{
		"the quick brown fox",
		"test_string_value",
		"another test message",
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