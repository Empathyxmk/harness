package original

import (
	"testing"
)

func TestBasicEncryptDecrypt(t *testing.T) {
	password := "password"
	message := "hello world"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt error: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("expected %q, got %q", message, decryptedMsg)
	}
}

func TestEncryptDecrypt_EmptyString(t *testing.T) {
	password := "password"
	message := ""
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt error: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("expected %q, got %q", message, decryptedMsg)
	}
}

func TestEncryptDecrypt_NonAscii(t *testing.T) {
	password := "password"
	message := "こんにちは世界" // "Hello World" in Japanese
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	decryptedMsg, err := Decrypt(password, encryptedMsg)
	if err != nil {
		t.Fatalf("decrypt error: %v", err)
	}
	if decryptedMsg != message {
		t.Errorf("expected %q, got %q", message, decryptedMsg)
	}
}

func TestDecrypt_WrongPassword(t *testing.T) {
	password := "password"
	wrongPassword := "notMyPassword"
	message := "hello world"
	encryptedMsg, err := Encrypt(password, message)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	_, err = Decrypt(wrongPassword, encryptedMsg)
	if err == nil {
		t.Fatalf("Expected error for wrong password, got nil")
	}
}

func TestDecrypt_InvalidBase64(t *testing.T) {
	password := "password"
	invalidBase64 := "not_base64!"
	_, err := Decrypt(password, invalidBase64)
	if err == nil {
		t.Fatalf("Expected error for invalid base64, got nil")
	}
}

func TestDecrypt_InvalidData(t *testing.T) {
	password := "password"
	invalidData := "MTIzNA==" // "1234" base64
	_, err := Decrypt(password, invalidData)
	if err == nil {
		t.Fatalf("Expected error for invalid data, got nil")
	}
}

func TestEncryptDecrypt_NullPassword(t *testing.T) {
	message := "hello"
	_, err := Encrypt("", message)
	if err == nil {
		t.Fatal("Expected error for empty password")
	}
}

func TestEncryptDecrypt_NullMessage(t *testing.T) {
	password := "pw"
	_, err := Encrypt(password, "")
	if err != nil {
		t.Fatal("Expected error for empty message")
	}
}

func TestDirectEncryptDecrypt(t *testing.T) {
	pw := "testing"
	msg := "msg"
	encrypted, err := Encrypt(pw, msg)
	if err != nil {
		t.Fatalf("encrypt error: %v", err)
	}
	decrypted, err := Decrypt(pw, encrypted)
	if err != nil {
		t.Fatalf("decrypt error: %v", err)
	}
	if decrypted != msg {
		t.Errorf("expected %q, got %q", msg, decrypted)
	}
}