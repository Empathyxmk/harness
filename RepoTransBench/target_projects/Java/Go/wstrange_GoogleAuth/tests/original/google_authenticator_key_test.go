package original

import (
	"reflect"
	"testing"
)

type GoogleAuthenticatorKeyGo2 struct {
	Config           GoogleAuthenticatorConfig
	SecretKey        string
	VerificationCode int
	ScratchCodes     []int
}

func newGoogleAuthenticatorKey(config GoogleAuthenticatorConfig, key string, code int, scratchCodes []int) GoogleAuthenticatorKeyGo2 {
	return GoogleAuthenticatorKeyGo2{
		Config:           config,
		SecretKey:        key,
		VerificationCode: code,
		ScratchCodes:     scratchCodes,
	}
}

func TestConstructorAndGetters(t *testing.T) {
	config := NewGoogleAuthenticatorConfig()
	key := "SECRETKEY"
	verificationCode := 123456
	scratchCodes := []int{111, 222}

	gak := newGoogleAuthenticatorKey(config, key, verificationCode, scratchCodes)
	if gak.SecretKey != key {
		t.Errorf("Expected SecretKey %s, got %s", key, gak.SecretKey)
	}
	if gak.VerificationCode != verificationCode {
		t.Errorf("Expected VerificationCode %d, got %d", verificationCode, gak.VerificationCode)
	}
	if !reflect.DeepEqual(gak.ScratchCodes, scratchCodes) {
		t.Errorf("Expected ScratchCodes %v, got %v", scratchCodes, gak.ScratchCodes)
	}
}

func TestEmptyScratchCodes(t *testing.T) {
	config := NewGoogleAuthenticatorConfig()
	key := "FOO"
	verificationCode := 0
	scratchCodes := []int{} // empty

	gak := newGoogleAuthenticatorKey(config, key, verificationCode, scratchCodes)
	if gak.SecretKey != key {
		t.Errorf("Expected SecretKey %s, got %s", key, gak.SecretKey)
	}
	if gak.VerificationCode != verificationCode {
		t.Errorf("Expected VerificationCode %d, got %d", verificationCode, gak.VerificationCode)
	}
	if !reflect.DeepEqual(gak.ScratchCodes, scratchCodes) {
		t.Errorf("Expected ScratchCodes %v, got %v", scratchCodes, gak.ScratchCodes)
	}
}