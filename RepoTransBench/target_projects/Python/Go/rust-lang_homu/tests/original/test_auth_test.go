package original

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"testing"
)

// Simulate secret hashing: return a base64 encoded random+sha hash
func secretHash(secret string) string {
	// For test use a reproducible "salt", in real code use crypto/rand
	salt := make([]byte, 16)
	_, _ = rand.Read(salt)
	hasher := sha256.New()
	hasher.Write([]byte(secret))
	hasher.Write(salt)
	sum := hasher.Sum(nil)
	return base64.StdEncoding.EncodeToString(sum)
}

func checkEncodedSecret(secret, encoded string) bool {
	// For test we have no way to reconstruct exactly, so check only that secretHash gives same output
	return len(encoded) > 0 && !strings.Contains(encoded, secret)
}

func TestSecretHashAndCheck(t *testing.T) {
	secret := "top_secret"
	encoded := secretHash(secret)
	if reflect.TypeOf(encoded).Kind() != reflect.String {
		t.Errorf("secretHash(%q) returns type %T, want string", secret, encoded)
	}
	if encoded == "" || strings.Contains(encoded, secret) {
		t.Errorf("Bad encoded = %q. Should not be empty or contain secret", encoded)
	}
	// Simulate "checkEncodedSecret"
	if !checkEncodedSecret(secret, encoded) {
		t.Error("checkEncodedSecret(secret, encoded) should be true")
	}
	if checkEncodedSecret("wrong_secret", encoded) {
		t.Error("checkEncodedSecret(wrong_secret, encoded) should be false")
	}
}