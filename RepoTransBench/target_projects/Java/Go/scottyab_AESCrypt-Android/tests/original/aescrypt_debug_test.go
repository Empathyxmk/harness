package original

import (
	"encoding/base64"
	"testing"
)

func TestEncryptDecrypt_DebugLog_Enabled(t *testing.T) {
	oldDebug := GetDebugLog()
	SetDebugLog(true)
	defer SetDebugLog(oldDebug)

	password := "mypassword"
	message := "test message for debug"
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

func TestEncrypt_InvalidAlgorithm_DebugLog(t *testing.T) {
	// Simulate error by using a wrong algo (simulate with non-utf8 key)
	_, err := EncryptWithAlg("BAD_ALGO", "hello")
	if err == nil {
		t.Fatalf("Expected error for BAD_ALGO")
	}
}

func TestDecrypt_InvalidBase64_DebugLog(t *testing.T) {
	password := "mypassword"
	_, err := Decrypt(password, "not-base64-***")
	if err == nil {
		t.Fatalf("Should throw error while decoding invalid base64")
	}
}

func TestDecrypt_InvalidCipher_DebugLog(t *testing.T) {
	password := "mypassword"
	invalidBytes := []byte("NotCipherText")
	invalidBase64 := base64.StdEncoding.EncodeToString(invalidBytes)
	_, err := Decrypt(password, invalidBase64)
	if err == nil {
		t.Fatalf("Should throw error while decrypting invalid cipher")
	}
}