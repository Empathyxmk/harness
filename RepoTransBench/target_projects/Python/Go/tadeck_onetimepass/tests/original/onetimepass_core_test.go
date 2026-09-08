package original

import (
	"bytes"
	"encoding/base32"
	"encoding/binary"
	"encoding/hex"
	"errors"
	"testing"
	"tadeck_onetimepass/onetimepass"
)

// Helper: monkeypatch time (simulate fixed time for deterministic TOTP tests)
func withFakeTime(t *testing.T, fake int64, fn func()) {
	orig := onetimepass.TimeNow
	onetimepass.TimeNow = func() int64 { return fake }
	defer func() { onetimepass.TimeNow = orig }()
	fn()
}

func TestIsPossibleTokenAcceptsValidAndInvalid(t *testing.T) {
	cases := []struct {
		value      interface{}
		shouldPass bool
	}{
		{123456, true},
		{[]byte("123456"), true},
		{"123456", true},
		{[]byte("abcdef"), false},
		{[]byte("12345678"), false},
		{"", false}, // empty string not possible
	}
	for _, c := range cases {
		if onetimepass.IsPossibleToken(c.value) != c.shouldPass {
			t.Errorf("IsPossibleToken(%#v) = %v, want %v", c.value, !c.shouldPass, c.shouldPass)
		}
	}
}

func TestGetHOTPTokenLengthAndInvalidSecret(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	result, err := onetimepass.GetHOTP(secret, 10, onetimepass.HOTPOptions{TokenLength: 8, AsString: true})
	if err != nil {
		t.Fatalf("GetHOTP returned error: %v", err)
	}
	switch res := result.(type) {
	case string:
		if len(res) != 8 {
			t.Errorf("GetHOTP returned string of len %d, want 8", len(res))
		}
	case []byte:
		if len(res) != 8 {
			t.Errorf("GetHOTP returned bytes of len %d, want 8", len(res))
		}
	default:
		t.Errorf("GetHOTP returned type %T, expected string or []byte", result)
	}

	// Should error for invalid base32 secret
	_, err = onetimepass.GetHOTP([]byte("invalid!!!!"), 1, onetimepass.HOTPOptions{})
	if err == nil {
		t.Error("Expected error for invalid base32 secret, got nil")
	}
}

func TestGetHOTPCasefoldFalse(t *testing.T) {
	secret := []byte("mfrggzdfmztwq2lk")
	// lower case only works with CaseFold:true
	_, err := onetimepass.GetHOTP(secret, 1, onetimepass.HOTPOptions{CaseFold: true})
	if err != nil {
		t.Errorf("Unexpected error (casefold true): %v", err)
	}
	_, err = onetimepass.GetHOTP(secret, 1, onetimepass.HOTPOptions{CaseFold: false})
	if err == nil {
		t.Errorf("Expected error with lower case base32 and casefold false")
	}
}

func TestTOTPDefault(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	tok, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{})
	if err != nil {
		t.Fatalf("GetTOTP error: %v", err)
	}
	if _, ok := tok.(int); !ok {
		t.Errorf("TOTP token is not int")
	}
	fakeTime := int64(1650000000)
	withFakeTime(t, fakeTime, func() {
		token, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{})
		if err != nil {
			t.Errorf("GetTOTP error with faked time: %v", err)
		}
		if _, ok := token.(int); !ok {
			t.Errorf("TOTP token from faked time is not int")
		}
	})
}

func TestValidHOTPAndLast(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	token, err := onetimepass.GetHOTP(secret, 2, onetimepass.HOTPOptions{})
	if err != nil {
		t.Fatalf("GetHOTP error: %v", err)
	}
	if i := onetimepass.ValidHOTP(token, secret, onetimepass.ValidHOTPOptions{}); i != 2 {
		t.Errorf("ValidHOTP should return 2, got %v", i)
	}
	if ok := onetimepass.ValidHOTP(token, secret, onetimepass.ValidHOTPOptions{Last: 2}); ok != false {
		t.Errorf("ValidHOTP with last=2 should be false, got %v", ok)
	}
	if ok := onetimepass.ValidHOTP("abcdef", secret, onetimepass.ValidHOTPOptions{}); ok != false {
		t.Errorf("ValidHOTP with impossible token should be false")
	}
	_, err = onetimepass.ValidHOTP(token, []byte("invalidsecret!!!!!"), onetimepass.ValidHOTPOptions{})
	if err == nil {
		t.Errorf("ValidHOTP with invalid secret should error")
	}
}

func TestGetTOTPTokenLengthAndString(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	fakeTime := int64(1650000000)
	withFakeTime(t, fakeTime, func() {
		result, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{TokenLength: 8, AsString: true})
		if err != nil {
			t.Fatalf("GetTOTP error: %v", err)
		}
		switch res := result.(type) {
		case string:
			if len(res) != 8 {
				t.Errorf("Returned string token len %d, want 8", len(res))
			}
		case []byte:
			if len(res) != 8 {
				t.Errorf("Returned byte token len %d, want 8", len(res))
			}
		default:
			t.Errorf("Returned token type %T, expected string/[]byte", result)
		}
	})
}

func TestValidTOTPAndWindow(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	fakeTime := int64(1650000000)
	withFakeTime(t, fakeTime, func() {
		token, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{})
		if err != nil {
			t.Fatalf("GetTOTP error: %v", err)
		}
		if !onetimepass.ValidTOTP(token, secret, onetimepass.ValidTOTPOptions{}) {
			t.Errorf("ValidTOTP should pass for exact token")
		}
		if !onetimepass.ValidTOTP(token, secret, onetimepass.ValidTOTPOptions{Window: 1}) {
			t.Errorf("ValidTOTP should pass for window=1")
		}
		if onetimepass.ValidTOTP(token.(int)+1, secret, onetimepass.ValidTOTPOptions{}) {
			t.Errorf("ValidTOTP should fail for wrong token")
		}
		if onetimepass.ValidTOTP("abcdef", secret, onetimepass.ValidTOTPOptions{}) {
			t.Errorf("ValidTOTP should fail for impossible token")
		}
		_, err = onetimepass.ValidTOTP(token, []byte("invalidsecret!!!"), onetimepass.ValidTOTPOptions{})
		if err == nil {
			t.Errorf("Expected error for invalid secret in ValidTOTP")
		}
	})
}

func TestGetTOTPFakeTime(t *testing.T) {
	secret := []byte("MFRGGZDFMZTWQ2LK")
	fakeTime := int64(1000)
	withFakeTime(t, fakeTime, func() {
		token, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{})
		if err != nil {
			t.Fatalf("GetTOTP error: %v", err)
		}
		if _, ok := token.(int); !ok {
			t.Errorf("TOTP token should be int (got %T)", token)
		}
	})
}