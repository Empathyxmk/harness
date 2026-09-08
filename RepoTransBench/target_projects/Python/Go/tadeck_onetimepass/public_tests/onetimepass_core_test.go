package public_tests

import (
	"testing"
	"tadeck_onetimepass/onetimepass"
)

func TestGetTOTP(t *testing.T) {
	secret := "12345678901234567890"
	code, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{TimeStep: 30, T: 1600000000})
	if err != nil {
		t.Fatalf("GetTOTP error: %v", err)
	}
	icode, ok := code.(int)
	if !ok {
		t.Fatalf("Expected int TOTP, got %T", code)
	}
	if !(icode >= 100000 && icode < 1000000) {
		t.Errorf("TOTP code = %d, want 6 digits", icode)
	}
}

func TestValidTOTPToken(t *testing.T) {
	secret := "22222222222222222222"
	code, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{T: 1600001000})
	if err != nil {
		t.Fatalf("GetTOTP error: %v", err)
	}
	if !onetimepass.ValidTOTP(code, secret, onetimepass.ValidTOTPOptions{Window: 0, T: 1600001000}) {
		t.Errorf("ValidTOTP failed for token just generated")
	}
}

func TestInvalidTOTPToken(t *testing.T) {
	secret := "33333333333333333333"
	code, err := onetimepass.GetTOTP(secret, onetimepass.TOTPOptions{T: 1600010000})
	if err != nil {
		t.Fatalf("GetTOTP error: %v", err)
	}
	icode, _ := code.(int)
	wrong := (icode + 10) % 1000000
	if onetimepass.ValidTOTP(wrong, secret, onetimepass.ValidTOTPOptions{Window: 0, T: 1600010000}) {
		t.Errorf("ValidTOTP should fail for incorrect token")
	}
}

func TestGetHOTP(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXP"
	code, err := onetimepass.GetHOTP(secret, 7, onetimepass.HOTPOptions{})
	if err != nil {
		t.Fatalf("GetHOTP error: %v", err)
	}
	icode, ok := code.(int)
	if !ok {
		t.Fatalf("Expected int HOTP, got %T", code)
	}
	if !(icode >= 100000 && icode < 1000000) {
		t.Errorf("HOTP code = %d, want 6 digits", icode)
	}
}

func TestValidHOTPTrue(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXQ"
	code, err := onetimepass.GetHOTP(secret, 42, onetimepass.HOTPOptions{})
	if err != nil {
		t.Fatalf("GetHOTP error: %v", err)
	}
	if !onetimepass.ValidHOTP(code, secret, onetimepass.ValidHOTPOptions{IntervalsNo: 42}) {
		t.Errorf("ValidHOTP should return true for correct code")
	}
}

func TestValidHOTPFalse(t *testing.T) {
	secret := "JBSWY3DPEHPK3PXR"
	code, err := onetimepass.GetHOTP(secret, 53, onetimepass.HOTPOptions{})
	if err != nil {
		t.Fatalf("GetHOTP error: %v", err)
	}
	icode, _ := code.(int)
	if onetimepass.ValidHOTP(icode+1, secret, onetimepass.ValidHOTPOptions{IntervalsNo: 53}) {
		t.Errorf("ValidHOTP should return false for incorrect code")
	}
}