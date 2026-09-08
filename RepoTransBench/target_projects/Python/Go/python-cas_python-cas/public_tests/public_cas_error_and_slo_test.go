package public_tests

import (
	"testing"
	"casproject/cas"
	"strings"
)

func TestCASErrorStrPublic(t *testing.T) {
	err := cas.NewCASError("another_fail")
	if err.Error() != "another_fail" {
		t.Errorf("Expected 'another_fail', got '%s'", err.Error())
	}
}

func TestSLOGetSAMLSLOsInvalidXMLPublic(t *testing.T) {
	invalidXML := "<xml broken"
	result := cas.SingleLogoutMixinGetSAMLSLOs(invalidXML)
	if result != nil {
		t.Errorf("Expected nil for broken xml")
	}
}

func TestSLOGetSAMLSLOsValidXMLPublic(t *testing.T) {
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-999-SLO</samlp:SessionIndex></samlp:LogoutRequest>`
	result := cas.SingleLogoutMixinGetSAMLSLOs(validXML)
	if len(result) != 1 {
		t.Errorf("Expected one session index, got %d", len(result))
	}
}

func TestSLOVerifyLogoutRequestTruePublic(t *testing.T) {
	validTicket := "ST-999-SLO"
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"><samlp:SessionIndex>` + validTicket + `</samlp:SessionIndex></samlp:LogoutRequest>`
	if !cas.SingleLogoutMixinVerifyLogoutRequest(validXML, validTicket) {
		t.Errorf("Expected true for matching ticket")
	}
}

func TestSLOVerifyLogoutRequestFalsePublic(t *testing.T) {
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"><samlp:SessionIndex>ST-555</samlp:SessionIndex></samlp:LogoutRequest>`
	ticket := "ST-999"
	if cas.SingleLogoutMixinVerifyLogoutRequest(validXML, ticket) {
		t.Errorf("Expected false for non-matching ticket")
	}
}

func TestSLOVerifyLogoutRequestInvalidXMLPublic(t *testing.T) {
	if cas.SingleLogoutMixinVerifyLogoutRequest("<broken <xml>", "otherticket") {
		t.Errorf("Expected false for invalid xml in verify logout request")
	}
}