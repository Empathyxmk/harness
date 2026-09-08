package public_tests

import (
	"testing"
)

func TestEncryptDecryptPublic(t *testing.T) {
	password := "anotherSecret"
	message := "public test string!"

	SetDebugLog(true)

	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("error occurred during encrypt in public test: %v", err)
	}

	messageAfterDecrypt, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("error occurred during decrypt in public test: %v", err)
	}

	if messageAfterDecrypt != message {
		t.Errorf("messages don't match after encrypt and decrypt in public test: got %q, want %q", messageAfterDecrypt, message)
	}
}

func TestEncryptPublic(t *testing.T) {
	password := "publicPass"
	message := "anotherMessage"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("error occurred during encrypt in public test: %v", err)
	}
	if encryptedMsg == "" {
		t.Error("encryptedMsg should not be empty")
	}
}

func TestDecryptPublic(t *testing.T) {
	password := "somePassword"
	encryptedMsg := "i5OSk38FnX6OGv5CeXf2iA=="
	result, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("error occurred during decrypt in public test: %v", err)
	}
	if result != "testOne" {
		t.Errorf("expected 'testOne', got %q", result)
	}
}