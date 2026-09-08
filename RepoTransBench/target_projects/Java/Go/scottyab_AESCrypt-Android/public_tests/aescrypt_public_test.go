package public_tests

import (
	"testing"
)

func TestEncryptDecryptWithDifferentDataPublic(t *testing.T) {
	password := "321secret"
	message := "Public AESCrypt test 42."
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("error on encrypt: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("error on decrypt: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("Public test value mismatch: got %q, want %q", decryptedMsg, message)
	}
}

func TestDecryptPrecomputedCiphertextPublic(t *testing.T) {
	password := "public123"
	encryptedMsg := "Ru4RNkDqQboiRkHi7U0koA=="
	result, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("error decrypting precomputed: %v", err)
	}
	if result != "helloPublic" {
		t.Errorf("expected helloPublic, got %q", result)
	}
}

func TestEncryptDecryptEmptyStringPublic(t *testing.T) {
	password := "emptyCase"
	message := ""
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt failed: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt failed: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("expected %q, got %q", message, decryptedMsg)
	}
}

func TestEncryptDecryptWithSpecialCharactersPublic(t *testing.T) {
	password := "specialP@sswørd"
	message := "!@#$%^&*()_+-=[]{};':,.<>/?`~"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt failed: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt failed: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("expected %q, got %q", message, decryptedMsg)
	}
}

func TestDecryptFailWithWrongPasswordPublic(t *testing.T) {
	password := "correctPassword"
	wrongPassword := "incorrectPassword"
	message := "Mismatch password public"
	encrypted, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	_, err = Decrypt(wrongPassword, encrypted)
	if err == nil {
		t.Fatalf("Should throw error for wrong password, got nil")
	}
}