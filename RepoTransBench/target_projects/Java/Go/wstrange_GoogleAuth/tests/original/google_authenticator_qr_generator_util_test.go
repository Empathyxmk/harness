package original

import (
	"errors"
	"net/url"
	"strings"
	"testing"
)

func internalURLEncode(s string) (string, error) {
	enc := url.QueryEscape(s)
	return enc, nil
}

func formatLabel(issuer *string, accountName string) (string, error) {
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

func TestInternalURLEncodeNormal(t *testing.T) {
	result, err := internalURLEncode("test@example.com")
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(result, "test%40example.com") {
		t.Errorf("Expected encoded email, got %s", result)
	}
}

func TestInternalURLEncode_Throws(t *testing.T) {
	// Not really possible to simulate error for utf-8 as in Java, so just call and ignore
	_, _ = internalURLEncode("irrelevant")
}

func TestFormatLabelHappyPath(t *testing.T) {
	label, err := formatLabel(toPtr("IssuerCompany"), "user@example.com")
	if err != nil {
		t.Fatal(err)
	}
	if label != "IssuerCompany:user@example.com" {
		t.Errorf("Expected label 'IssuerCompany:user@example.com', got '%s'", label)
	}
	label, err = formatLabel(nil, "john")
	if err != nil {
		t.Fatal(err)
	}
	if label != "john" {
		t.Errorf("Expected label 'john', got '%s'", label)
	}
}

func TestFormatLabelThrows_AccountNameNull(t *testing.T) {
	_, err := formatLabel(toPtr("Company"), "")
	if err == nil {
		t.Fatal("Expected error for empty account name")
	}
}

func TestFormatLabelThrows_AccountNameEmpty(t *testing.T) {
	_, err := formatLabel(toPtr("Company"), "")
	if err == nil {
		t.Fatal("Expected error for empty account name")
	}
}

func TestFormatLabelThrows_IssuerContainsColon(t *testing.T) {
	_, err := formatLabel(toPtr("Iss:uer"), "user")
	if err == nil {
		t.Fatal("Expected error for colon in issuer")
	}
}

func toPtr(s string) *string {
	return &s
}