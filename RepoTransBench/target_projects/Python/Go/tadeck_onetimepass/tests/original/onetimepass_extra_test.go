package original

import (
	"testing"
	"tadeck_onetimepass/onetimepass"
	"crypto/sha256"
	"bytes"
)

func TestGetHOTPInvalidSecretType(t *testing.T) {
	_, err := onetimepass.GetHOTP(1234, 1, onetimepass.HOTPOptions{})
	if err == nil {
		t.Errorf("Expected error for secret of invalid type (int), got nil")
	}
}

func TestGetHOTPIncorrectBase32(t *testing.T) {
	_, err := onetimepass.GetHOTP([]byte("notbase32@#$"), 1, onetimepass.HOTPOptions{})
	if err == nil {
		t.Errorf("GetHOTP should error for non-base32 input")
	}
}

func TestGetHOTPCustomDigest(t *testing.T) {
	val, err := onetimepass.GetHOTP([]byte("MFRGGZDFMZTWQ2LK"), 1, onetimepass.HOTPOptions{DigestMethod: sha256.New, TokenLength: 8})
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	// Should return int up to 8 digits
	if _, ok := val.(int); !ok {
		t.Errorf("Expected int HOTP token, got %T", val)
	}
	if l := len(bytes.Trim([]byte(string(val.(int))), " ")); l > 8 {
		t.Errorf("Custom digest HOTP should be at most 8 digits, got len %d", l)
	}
}

func TestGetHOTPStringTypes(t *testing.T) {
	res, err := onetimepass.GetHOTP("MFRGGZDFMZTWQ2LK", 2, onetimepass.HOTPOptions{AsString: true})
	if err != nil {
		t.Fatalf("GetHOTP error: %v", err)
	}
	rb, ok := res.([]byte)
	if ok {
		expect := []byte("816065")
		if !bytes.Equal(rb, expect) {
			t.Errorf("Expected HOTP string token %v, got %v", expect, rb)
		}
	} else {
		t.Errorf("GetHOTP returned type %T, want []byte", res)
	}
}

func TestValidHOTPReturnsFalse(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	if ok := onetimepass.ValidHOTP(111111, secret, onetimepass.ValidHOTPOptions{Last: 0, Trials: 1}); ok != false {
		t.Errorf("ValidHOTP on unlikely token should return false")
	}
}

func TestValidHOTPWithRange(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	tok, _ := onetimepass.GetHOTP(secret, 99, onetimepass.HOTPOptions{})
	got := onetimepass.ValidHOTP(tok, secret, onetimepass.ValidHOTPOptions{Last: 97, Trials: 3})
	if got != 99 {
		t.Errorf("Expected ValidHOTP(...) == 99, got %v", got)
	}
}

func TestValidTOTPFalse(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	if onetimepass.ValidTOTP(123456, secret, onetimepass.ValidTOTPOptions{}) {
		t.Errorf("ValidTOTP should return false for random token")
	}
}

func TestGetTOTPAndValidTOTP(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	tok, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{})
	if err != nil {
		t.Fatalf("GetTOTP error: %v", err)
	}
	if !onetimepass.ValidTOTP(tok, secret, onetimepass.ValidTOTPOptions{}) {
		t.Errorf("ValidTOTP(..., correct token) = false, want true")
	}
	if onetimepass.ValidTOTP(tok.(int)+1, secret, onetimepass.ValidTOTPOptions{}) {
		t.Errorf("ValidTOTP with off-by-one should be false")
	}
}

func TestGetTOTPCustomTokenLength(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	tok, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{TokenLength: 8})
	if err != nil {
		t.Fatalf("GetTOTP error: %v", err)
	}
	if _, ok := tok.(int); !ok {
		t.Errorf("Expected TOTP int token, got %T", tok)
	}
	if l := len([]byte(string(tok.(int)))); l > 8 {
		t.Errorf("TOTP token should be at most 8 digits, got %d", l)
	}
}