package public_tests

import (
	"testing"

	. "orcasgit_django_fernet_fields/tests"
)

func TestFernetFieldEncryptDecrypt_Public(t *testing.T) {
	field := NewFernetField()
	data := []byte("SensitivePublicData123")
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

func TestFernetFieldDifferentData_Public(t *testing.T) {
	field := NewFernetField()
	value := []byte("UniqueBytesForPublicTest")
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

func TestFernetFieldHandlesEmptyBytes_Public(t *testing.T) {
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

func TestFernetFieldParametrize_Public(t *testing.T) {
	testCases := [][]byte{
		[]byte("public_param_1"),
		[]byte("another_param_public_2"),
		[]byte("extra_data_public_3"),
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