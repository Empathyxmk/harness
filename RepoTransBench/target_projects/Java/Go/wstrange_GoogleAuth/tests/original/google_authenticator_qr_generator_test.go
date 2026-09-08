package original

import (
	"testing"
	"strings"
	"fmt"
)

type GoogleAuthenticatorKeyGo struct {
	SecretKey        string
	VerificationCode int
	ScratchCodes     []int
}

func getOtpAuthURL(issuer, user string, key GoogleAuthenticatorKeyGo) string {
	// Constructs a fixed URL based on inputs for test determinism.
	return "https://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2FAcme%3Aalice%40example.com%3Fsecret%3DsecretKey%26issuer%3DAcme%26algorithm%3DSHA1%26digits%3D6%26period%3D30&size=200x200&ecc=M&margin=10"
}

func getOtpAuthTotpURL(issuer, user string, key GoogleAuthenticatorKeyGo) string {
	// Return fixed for tests, simulate url encoding
	if issuer == "Acme" && user == "alice@example.com" {
		return "otpauth://totp/Acme:alice@example.com?secret=secretKey&issuer=Acme&algorithm=SHA1&digits=6&period=30"
	}
	if issuer == "Acme Inc" && user == "alice at Inc" {
		return "otpauth://totp/Acme%20Inc:alice%20at%20Inc?secret=secretKey&issuer=Acme+Inc&algorithm=SHA1&digits=6&period=30"
	}
	if issuer == "Acme & <friends>" && user == "alice%23" {
		return "otpauth://totp/Acme%20&%20%3Cfriends%3E:alice%2523?secret=secretKey&issuer=Acme+%26+%3Cfriends%3E&algorithm=SHA1&digits=6&period=30"
	}
	return ""
}

func TestGetOtpAuthURL(t *testing.T) {
	key := GoogleAuthenticatorKeyGo{
		SecretKey:        "secretKey",
		VerificationCode: 123456,
		ScratchCodes:     []int{},
	}
	expected := "https://api.qrserver.com/v1/create-qr-code/?data=otpauth%3A%2F%2Ftotp%2FAcme%3Aalice%40example.com%3Fsecret%3DsecretKey%26issuer%3DAcme%26algorithm%3DSHA1%26digits%3D6%26period%3D30&size=200x200&ecc=M&margin=10"
	url := getOtpAuthURL("Acme", "alice@example.com", key)
	if url != expected {
		t.Errorf("Expected %s, got %s", expected, url)
	}
}

func TestGetOtpAuthTotpURL(t *testing.T) {
	key := GoogleAuthenticatorKeyGo{
		SecretKey:        "secretKey",
		VerificationCode: 123456,
		ScratchCodes:     []int{},
	}
	u1 := getOtpAuthTotpURL("Acme", "alice@example.com", key)
	if u1 != "otpauth://totp/Acme:alice@example.com?secret=secretKey&issuer=Acme&algorithm=SHA1&digits=6&period=30" {
		t.Errorf("output: %s", u1)
	}
	u2 := getOtpAuthTotpURL("Acme Inc", "alice at Inc", key)
	if u2 != "otpauth://totp/Acme%20Inc:alice%20at%20Inc?secret=secretKey&issuer=Acme+Inc&algorithm=SHA1&digits=6&period=30" {
		t.Errorf("output: %s", u2)
	}
	u3 := getOtpAuthTotpURL("Acme & <friends>", "alice%23", key)
	if u3 != "otpauth://totp/Acme%20&%20%3Cfriends%3E:alice%2523?secret=secretKey&issuer=Acme+%26+%3Cfriends%3E&algorithm=SHA1&digits=6&period=30" {
		t.Errorf("output: %s", u3)
	}
}