package public_tests

import (
	"testing"
	"tadeck_onetimepass/onetimepass"
)

func TestSecretToBase32(t *testing.T) {
	secret := []byte("different secret")
	b32, err := onetimepass.SecretToBase32(secret)
	if err != nil {
		t.Fatalf("SecretToBase32 error: %v", err)
	}
	if len(b32) == 0 {
		t.Errorf("secret_to_base32 returned empty string")
	}
	for _, c := range b32 {
		if !((c >= 'A' && c <= 'Z') || (c >= '2' && c <= '7') || c == '=') {
			t.Errorf("Invalid character %q in base32 result", c)
		}
	}
}

func TestValidBase32ReturnTypes(t *testing.T) {
	if !onetimepass.ValidBase32("MFRGGZDFMZRW63LQ") {
		t.Errorf("ValidBase32 should be true for valid base32")
	}
	if onetimepass.ValidBase32("123#XYZ") {
		t.Errorf("ValidBase32 should be false for invalid string")
	}
}

func TestGenerateNewSecretLength(t *testing.T) {
	secret8, err := onetimepass.GenerateNewSecret(8)
	if err != nil {
		t.Fatalf("GenerateNewSecret(8) failed: %v", err)
	}
	secret24, err := onetimepass.GenerateNewSecret(24)
	if err != nil {
		t.Fatalf("GenerateNewSecret(24) failed: %v", err)
	}
	if len(secret8) != 8 {
		t.Errorf("GenerateNewSecret(8) = %q (len %d)", secret8, len(secret8))
	}
	if len(secret24) != 24 {
		t.Errorf("GenerateNewSecret(24) = %q (len %d)", secret24, len(secret24))
	}
}

func TestGenerateNewSecretBase32(t *testing.T) {
	secret, err := onetimepass.GenerateNewSecret(18)
	if err != nil {
		t.Fatalf("GenerateNewSecret(18) error: %v", err)
	}
	if !onetimepass.ValidBase32(secret) {
		t.Errorf("GenerateNewSecret did not return valid base32")
	}
}