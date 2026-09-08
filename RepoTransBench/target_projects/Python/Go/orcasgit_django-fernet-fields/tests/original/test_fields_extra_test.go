package original

import (
	"testing"

	. "orcasgit_django_fernet_fields/tests"
)

func TestFernetFieldEncryptDecrypt(t *testing.T) {
	field := NewFernetField()
	data := []byte("SensitiveData123")
	encrypted, err := field.GetPrepValue(data)
	if err != nil {
		t.Fatalf("Encryption failed: %v", err)
	}
	decrypted, err := field.FromDBValue(encrypted)
	if err != nil {
		t.Fatalf("Decryption failed: %v", err)
	}
	AssertBytesEqual(t, decrypted, data, "Decrypted bytes should match input bytes")
}

func TestFernetFieldDifferentData(t *testing.T) {
	field := NewFernetField()
	value := []byte("AnotherSecret")
	encrypted, err := field.GetPrepValue(value)
	if err != nil {
		t.Fatalf("Encryption failed: %v", err)
	}
	decrypted, err := field.FromDBValue(encrypted)
	if err != nil {
		t.Fatalf("Decryption failed: %v", err)
	}
	AssertBytesEqual(t, decrypted, value, "Decrypted bytes should match input bytes")
}

func TestFernetFieldHandlesEmptyBytes(t *testing.T) {
	field := NewFernetField()
	value := []byte("")
	encrypted, err := field.GetPrepValue(value)
	if err != nil {
		t.Fatalf("Encryption failed: %v", err)
	}
	decrypted, err := field.FromDBValue(encrypted)
	if err != nil {
		t.Fatalf("Decryption failed: %v", err)
	}
	AssertBytesEqual(t, decrypted, []byte(""), "Decrypted bytes should be empty")
}

func TestFernetFieldParametrize(t *testing.T) {
	testCases := [][]byte{
		[]byte("param_1"),
		[]byte("param_2"),
		[]byte("param_3"),
	}
	field := NewFernetField()
	for _, val := range testCases {
		encrypted, err := field.GetPrepValue(val)
		if err != nil {
			t.Fatalf("Encryption failed: %v", err)
		}
		decrypted, err := field.FromDBValue(encrypted)
		if err != nil {
			t.Fatalf("Decryption failed: %v", err)
		}
		AssertBytesEqual(t, decrypted, val, "Decrypted bytes should match input bytes")
	}
}