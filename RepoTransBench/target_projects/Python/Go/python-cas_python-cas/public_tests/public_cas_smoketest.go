package public_tests

import (
	"testing"
	"casproject/cas"
	"strings"
)

func TestSmoketestCASErrorPublic(t *testing.T) {
	e := cas.NewCASError("smoke_public")
	if e.Error() != "smoke_public" {
		t.Errorf("Expected error string == 'smoke_public', got %s", e.Error())
	}
}

func TestSmoketestSLOPublic(t *testing.T) {
	logoutXML := `<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol">
    <samlp:SessionIndex>ST-PUBLIC-777</samlp:SessionIndex></samlp:LogoutRequest>`
	sessionIndexes := cas.SingleLogoutMixinGetSAMLSLOs(logoutXML)
	if len(sessionIndexes) != 1 {
		t.Errorf("Expected one session index, got %d", len(sessionIndexes))
	}
	if sessionIndexes[0].Text != "ST-PUBLIC-777" {
		t.Errorf("Expected ST-PUBLIC-777, got %s", sessionIndexes[0].Text)
	}

	if !cas.SingleLogoutMixinVerifyLogoutRequest(logoutXML, "ST-PUBLIC-777") {
		t.Errorf("Expected verify logout request with matching ticket to be true")
	}
	if cas.SingleLogoutMixinVerifyLogoutRequest(logoutXML, "ST-PUBLIC-888") {
		t.Errorf("Expected verify logout request with wrong ticket to be false")
	}
}

func TestSmoketestClientBasePublic(t *testing.T) {
	cl := cas.NewCASClientBase(
		true,
		nil,
		"https://smoke.cas.org/server/",
		"https://smoke.cas.org/client/",
	)
	url := cl.GetLoginURL()
	if !strings.HasPrefix(url, "https://smoke.cas.org/server/login?") {
		t.Errorf("Expected login url prefix, got %s", url)
	}
	if !strings.Contains(url, "renew=true") {
		t.Errorf("Expected 'renew=true' param in login url, got %s", url)
	}
	out := cl.GetLogoutURL()
	if out != "https://smoke.cas.org/server/logout" {
		t.Errorf("Expected logout url, got %s", out)
	}
}