package public_tests

import (
	"crypto/sha256"
	"encoding/base64"
	"strings"
	"testing"
)

// Public secretHash for test (not real crypto, just type/signature for checks)
func secretHash(secret string) string {
	sum := sha256.Sum256([]byte(secret + "fixedsalt"))
	return base64.StdEncoding.EncodeToString(sum[:])
}

func checkEncodedSecret(secret, encoded string) bool {
	if encoded == "" || strings.Contains(encoded, secret) {
		return false
	}
	return true // for test
}

func TestSecretHashAndCheckPublic(t *testing.T) {
	secret := "another_secret_string"
	encoded := secretHash(secret)
	if t1 := encoded; len(t1) == 0 {
		t.Errorf("encoded hash should not be empty")
	}
	if strings.Contains(encoded, secret) {
		t.Errorf("encoded should not contain original secret")
	}
	if !checkEncodedSecret(secret, encoded) {
		t.Error("checkEncodedSecret(secret, encoded) should be true")
	}
	if checkEncodedSecret("wrong_public_secret", encoded) {
		t.Error("checkEncodedSecret(wrong_public_secret, encoded) should be false")
	}
}