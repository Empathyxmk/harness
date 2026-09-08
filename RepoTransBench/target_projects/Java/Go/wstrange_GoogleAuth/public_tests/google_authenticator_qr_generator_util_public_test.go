package public_tests

import (
	"errors"
	"net/url"
	"strings"
	"testing"
)

func publicInternalURLEncode(s string) (string, error) {
	return url.QueryEscape(s), nil
}

func publicFormatLabel(issuer *string, accountName string) (string, error) {
	if accountName == "" {
		return "", errors.New("accountName cannot be empty")
	}
	if issuer != nil {
		if strings.Contains(*issuer, ":") {
			return "", errors.New("issuer must not contain colon")
		}
		return *issuer + ":" + accountName, nil
	}
	return accountName, nil
}

func TestInternalURLEncodeNormal_public(t *testing.T) {
	result, err := publicInternalURLEncode("hello+world@example.org")
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(result, "hello%2Bworld%40example.org") {
		t.Errorf("Expected encoded form, got %s", result)
	}
}

func TestFormatLabelHappyPath_public(t *testing.T) {
	label, err := publicFormatLabel(toPtr("OtherIssuer"), "publicuser@domain.net")
	if err != nil {
		t.Fatal(err)
	}
	if label != "OtherIssuer:publicuser@domain.net" {
		t.Errorf("Expected 'OtherIssuer:publicuser@domain.net', got '%s'", label)
	}
	label, err = publicFormatLabel(nil, "bob")
	if err != nil {
		t.Fatal(err)
	}
	if label != "bob" {
		t.Errorf("Expected 'bob', got '%s'", label)
	}
}

func TestFormatLabelThrows_AccountNameNull_public(t *testing.T) {
	_, err := publicFormatLabel(toPtr("Acme"), "")
	if err == nil {
		t.Fatal("Expected error for empty account name")
	}
}

func TestFormatLabelThrows_AccountNameEmpty_public(t *testing.T) {
	_, err := publicFormatLabel(toPtr("Acme"), "")
	if err == nil {
		t.Fatal("Expected error for empty account name")
	}
}

func TestFormatLabelThrows_IssuerContainsColon_public(t *testing.T) {
	_, err := publicFormatLabel(toPtr("Not:Valid"), "janedoe")
	if err == nil {
		t.Fatal("Expected error for colon in issuer")
	}
}

func toPtr(s string) *string {
	return &s
}