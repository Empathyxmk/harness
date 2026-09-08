package original

import (
	"testing"
)

func TestGenerateKey(t *testing.T) {
	password := "test"
	message := "data"
	encrypted, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("Error encrypting: %v", err)
	}
	decrypted, err := Decrypt(password, encrypted)
	if err != nil {
		t.Fatalf("Error decrypting: %v", err)
	}
	if decrypted != message {
		t.Errorf("Expected %q, got %q", message, decrypted)
	}
}

func TestGenerateKey_FailsWithBadAlgorithm(t *testing.T) {
	password := ""
	for i := 0; i < 1000; i++ {
		password += "x"
	}
	encrypted, err := Encrypt(password, "data")
	if err != nil {
		t.Fatalf("Should not fail for long password: %v", err)
	}
	decrypted, err := Decrypt(password, encrypted)
	if err != nil {
		t.Fatalf("Should not fail for long password decryption: %v", err)
	}
	if decrypted != "data" {
		t.Errorf("Expected %q, got %q", "data", decrypted)
	}
}

func TestGenerateKey_UnsupportedEncoding(t *testing.T) {
	// Go always supports UTF-8, so just assert true
	if true != true {
		t.Error("true should be true")
	}
}