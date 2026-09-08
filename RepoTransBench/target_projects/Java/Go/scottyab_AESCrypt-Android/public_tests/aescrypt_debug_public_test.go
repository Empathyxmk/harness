package public_tests

import (
	"testing"
)

func TestEncryptDecryptWithDebugPublic(t *testing.T) {
	oldDebug := GetDebugLog()
	SetDebugLog(true)
	defer SetDebugLog(oldDebug)

	password := "pubDebugPass128"
	message := "Debug public test message with 128"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error in debug public: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt error in debug public: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("Debug public message failed: expected %q, got %q", message, decryptedMsg)
	}
}

func TestWrongPasswordDecryptionPublic(t *testing.T) {
	password := "pubDebugPassword"
	wrongPassword := "pubDebugWrongPwd"
	message := "Different message for debug"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("Encrypt should not throw in debug public test: %v", err)
	}
	_, err = Decrypt(wrongPassword, encryptedMsg)
	if err == nil {
		t.Fatalf("Expected error for wrong password in debug public test")
	}
}

func TestEncryptDecryptWithUnicodePublic(t *testing.T) {
	password := "Pública123!"
	message := "Тестовое сообщение 🌍"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt error: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("Unicode debug public message failed: expected %q, got %q", message, decryptedMsg)
	}
}