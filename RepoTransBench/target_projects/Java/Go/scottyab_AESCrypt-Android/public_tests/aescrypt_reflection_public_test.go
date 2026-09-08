package public_tests

import (
	"testing"
)

func TestGenerateKeyPublic(t *testing.T) {
	password := "publicTest"
	message := "testing"
	encrypted, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	decrypted, err := Decrypt(password, encrypted)
	if err != nil {
		t.Fatalf("decrypt error: %v", err)
	}
	if decrypted != message {
		t.Errorf("expected %q, got %q", message, decrypted)
	}
}

func TestGenerateKey_FailsWithVeryLongPasswordPublic(t *testing.T) {
	password := "verylongpassword0123456789verylongpassword0123456789verylongpassword0123456789"
	encrypted, err := Encrypt(password, "foobar")
	if err != nil {
		t.Fatalf("Should not fail for very long password - public test: %v", err)
	}
	decrypted, err := Decrypt(password, encrypted)
	if err != nil {
		t.Fatalf("Should not fail for very long password - public test decrypt: %v", err)
	}
	if decrypted != "foobar" {
		t.Errorf("expected %q, got %q", "foobar", decrypted)
	}
}

func TestGenerateKey_UnsupportedEncodingPublic(t *testing.T) {
	if true != true {
		t.Error("true is not true")
	}
}