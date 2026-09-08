package original

import (
	"testing"
)

func TestEncryptDecrypt(t *testing.T) {
	password := "password"
	message := "hello world"

	// Enable debug log if needed.
	SetDebugLog(true)

	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("error occurred during encrypt: %v", err)
	}

	messageAfterDecrypt, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("error occurred during decrypt: %v", err)
	}

	if messageAfterDecrypt != message {
		t.Fatalf("messages don't match after encrypt and decrypt: got %q, want %q", messageAfterDecrypt, message)
	}
}

func TestEncryt(t *testing.T) {
	password := "password"
	message := "hello world"

	_, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("error occurred during encrypt: %v", err)
	}
}

func TestDecrpyt(t *testing.T) {
	password := "password"
	encryptedMsg := "2B22cS3UC5s35WBihLBo8w=="

	_, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("error occurred during Decrypt: %v", err)
	}
}