package public_tests

import (
	"testing"
	"casproject/cas"
	"strings"
)

func TestExtraErrorTypePublic(t *testing.T) {
	x := cas.NewCASError("extra public error example")
	if !strings.Contains(x.Error(), "extra") {
		t.Errorf("Expected error to include 'extra', got '%s'", x.Error())
	}
}

func TestExtraLogoutMixinInvalidXMLPublic(t *testing.T) {
	invalidXML := "some completely invalid {{{"
	result := cas.SingleLogoutMixinGetSAMLSLOs(invalidXML)
	if result != nil {
		t.Errorf("Expected nil result for invalid XML, got %v", result)
	}
}

func TestExtraLogoutMixinValidXMLPublic(t *testing.T) {
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>EXTRA-222-SLO</samlp:SessionIndex></samlp:LogoutRequest>`
	result := cas.SingleLogoutMixinGetSAMLSLOs(validXML)
	if len(result) != 1 {
		t.Errorf("Expected one session index, got %d", len(result))
	}
	if result[0].Text != "EXTRA-222-SLO" {
		t.Errorf("Expected session index text EXTRA-222-SLO, got %s", result[0].Text)
	}
}