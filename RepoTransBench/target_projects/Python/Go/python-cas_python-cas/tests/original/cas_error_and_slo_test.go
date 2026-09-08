package original

import (
	"testing"
	"casproject/cas"
)

func TestCASErrorStr(t *testing.T) {
	err := cas.NewCASError("fail")
	if err.Error() != "fail" {
		t.Errorf("Expected error message 'fail', got '%s'", err.Error())
	}
}

func TestSLOGetSAMLSLOsInvalidXML(t *testing.T) {
	invalidXML := "<bad<xml>"
	result := cas.SingleLogoutMixinGetSAMLSLOs(invalidXML)
	if result != nil {
		t.Errorf("Expected nil result for invalid XML, got %v", result)
	}
}

func TestSLOGetSAMLSLOsValidXML(t *testing.T) {
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
		<samlp:SessionIndex>ST-123-SLO</samlp:SessionIndex></samlp:LogoutRequest>`
	result := cas.SingleLogoutMixinGetSAMLSLOs(validXML)
	if len(result) != 1 {
		t.Errorf("Expected 1 SLO session index, got %d", len(result))
	}
}

func TestSLOVerifyLogoutRequestTrue(t *testing.T) {
	validTicket := "ST-123-SLO"
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"><samlp:SessionIndex>` + validTicket + `</samlp:SessionIndex></samlp:LogoutRequest>`
	if !cas.SingleLogoutMixinVerifyLogoutRequest(validXML, validTicket) {
		t.Errorf("Expected true for matching session index and ticket in SLO XML")
	}
}

func TestSLOVerifyLogoutRequestFalse(t *testing.T) {
	validXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"><samlp:SessionIndex>ST-456</samlp:SessionIndex></samlp:LogoutRequest>`
	ticket := "ST-123"
	if cas.SingleLogoutMixinVerifyLogoutRequest(validXML, ticket) {
		t.Errorf("Expected false for non-matching session index and ticket in SLO XML")
	}
}

func TestSLOVerifyLogoutRequestInvalidXML(t *testing.T) {
	if cas.SingleLogoutMixinVerifyLogoutRequest("<bad<xml>", "anyticket") {
		t.Errorf("Expected false for invalid XML to VerifyLogoutRequest")
	}
}