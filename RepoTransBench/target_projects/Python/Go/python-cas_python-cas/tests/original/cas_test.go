package original

import (
	"strings"
	"testing"
	"casproject/cas"
)

func TestLoginURLHelper(t *testing.T) {
	client := cas.NewCASClientBase(
		false,
		nil,
		"http://www.example.com/cas/",
		"http://testserver/",
	)
	actual := client.GetLoginURL()
	expected := "http://www.example.com/cas/login?service=http%3A%2F%2Ftestserver%2F"
	if actual != expected {
		t.Errorf("Expected login url %s, got %s", expected, actual)
	}
}

func TestLoginURLHelperWithExtraParams(t *testing.T) {
	client := cas.NewCASClientBase(
		false,
		map[string]string{"test": "1234"},
		"http://www.example.com/cas/",
		"http://testserver/",
	)
	actual := client.GetLoginURL()
	if !strings.Contains(actual, "service=http%3A%2F%2Ftestserver%2F") || !strings.Contains(actual, "test=1234") {
		t.Errorf("Expected query params in login url, got %s", actual)
	}
}

func TestLoginURLHelperWithRenew(t *testing.T) {
	client := cas.NewCASClientBase(
		true,
		nil,
		"http://www.example.com/cas/",
		"http://testserver/",
	)
	actual := client.GetLoginURL()
	if !strings.Contains(actual, "service=http%3A%2F%2Ftestserver%2F") ||
		!strings.Contains(actual, "renew=true") {
		t.Errorf("Expected renew query param in login url, got %s", actual)
	}
}

func getLogoutClient(version string) *cas.CASClient {
	return cas.NewCASClient(version, "http://www.example.com/cas/", "")
}

func TestLogoutURL(t *testing.T) {
	client := getLogoutClient("3")
	actual := client.GetLogoutURL("")
	expected := "http://www.example.com/cas/logout"
	if actual != expected {
		t.Errorf("Expected logout url %s, got %s", expected, actual)
	}
}

func TestV1LogoutURLWithRedirect(t *testing.T) {
	client := getLogoutClient("1")
	actual := client.GetLogoutURL("http://testserver/landing-page/")
	expected := "http://www.example.com/cas/logout?url=http%3A%2F%2Ftestserver%2Flanding-page%2F"
	if actual != expected {
		t.Errorf("Expected v1 logout redirect url %s, got %s", expected, actual)
	}
}

func TestV2LogoutURLWithRedirect(t *testing.T) {
	client := getLogoutClient("2")
	actual := client.GetLogoutURL("http://testserver/landing-page/")
	expected := "http://www.example.com/cas/logout?url=http%3A%2F%2Ftestserver%2Flanding-page%2F"
	if actual != expected {
		t.Errorf("Expected v2 logout redirect url %s, got %s", expected, actual)
	}
}

func TestV3LogoutURLWithRedirect(t *testing.T) {
	client := getLogoutClient("3")
	actual := client.GetLogoutURL("http://testserver/landing-page/")
	expected := "http://www.example.com/cas/logout?service=http%3A%2F%2Ftestserver%2Flanding-page%2F"
	if actual != expected {
		t.Errorf("Expected v3 logout redirect url %s, got %s", expected, actual)
	}
}

func TestV3LogoutURLWithoutRedirect(t *testing.T) {
	client := getLogoutClient("3")
	actual := client.GetLogoutURL("")
	expected := "http://www.example.com/cas/logout"
	if actual != expected {
		t.Errorf("Expected v3 logout without redirect url %s, got %s", expected, actual)
	}
}

func getClientV3() *cas.CASClient {
	return cas.NewCASClient("3", "https://cas.example.com/cas/", "https://example.com/login")
}

const successResponse = `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>user@example.com</cas:user></cas:authenticationSuccess></cas:serviceResponse>
`

func TestCAS3BasicSuccessfulResponseVerification(t *testing.T) {
	user, attributes, pgtiou := getClientV3().VerifyResponse(successResponse)
	if user != "user@example.com" {
		t.Errorf("Expected user user@example.com, got %s", user)
	}
	if len(attributes) != 0 {
		t.Errorf("Expected attributes to be empty, got %v", attributes)
	}
	if pgtiou != "" {
		t.Errorf("Expected pgtiou to be empty, got %s", pgtiou)
	}
}

const successResponseWithAttributes = `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>user@example.com</cas:user><cas:attributes><cas:foo>bar</cas:foo><cas:baz>1234</cas:baz></cas:attributes></cas:authenticationSuccess></cas:serviceResponse>
`

func TestCAS3SuccessfulResponseVerificationWithAttributes(t *testing.T) {
	user, attributes, pgtiou := getClientV3().VerifyResponse(successResponseWithAttributes)
	if user != "user@example.com" {
		t.Errorf("Expected user user@example.com, got %s", user)
	}
	if pgtiou != "" {
		t.Errorf("Expected pgtiou to be empty, got %s", pgtiou)
	}
	if attributes["foo"] != "bar" || attributes["baz"] != "1234" {
		t.Errorf("Expected attributes to have foo='bar', baz='1234', got %v", attributes)
	}
}

const successResponseWithPGTIOU = `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>user@example.com</cas:user><cas:proxyGrantingTicket>PGTIOU-84678-8a9d</cas:proxyGrantingTicket></cas:authenticationSuccess></cas:serviceResponse>
`

func TestSuccessfulResponseVerificationWithPGTIOU(t *testing.T) {
	user, _, pgtiou := getClientV3().VerifyResponse(successResponseWithPGTIOU)
	if user != "user@example.com" {
		t.Errorf("Expected user user@example.com, got %s", user)
	}
	if pgtiou != "PGTIOU-84678-8a9d" {
		t.Errorf("Expected pgtiou to be PGTIOU-84678-8a9d, got %s", pgtiou)
	}
}

const failureResponse = `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationFailure code="INVALID_TICKET">service ticket ST-1415306486-qs5TfUWlwge23u013h8fivR21RklkeWI has already been used</cas:authenticationFailure></cas:serviceResponse>
`

func TestUnsuccessfulResponse(t *testing.T) {
	user, attributes, pgtiou := getClientV3().VerifyResponse(failureResponse)
	if user != "" {
		t.Errorf("Expected user to be empty for unsuccessful response")
	}
	if pgtiou != "" {
		t.Errorf("Expected pgtiou to be empty for unsuccessful response, got: %s", pgtiou)
	}
	if len(attributes) != 0 {
		t.Errorf("Expected attributes to be empty for unsuccessful response, got: %v", attributes)
	}
}

func TestProxyURL(t *testing.T) {
	client := getClientV3()
	tgt := "tgt-1234"
	proxyUrlString := client.GetProxyURL(tgt)
	opt1 := "https://cas.example.com/cas/proxy?pgt=tgt-1234&targetService=https%3A%2F%2Fexample.com%2Flogin"
	opt2 := "https://cas.example.com/cas/proxy?targetService=https%3A%2F%2Fexample.com%2Flogin&pgt=tgt-1234"
	if proxyUrlString != opt1 && proxyUrlString != opt2 {
		t.Errorf("Expected one of valid proxy URLs, got %s", proxyUrlString)
	}
}

func TestCanSAMLAssertionIsEncoded(t *testing.T) {
	ticket := "test-ticket"
	client := cas.NewCASClient("CAS_2_SAML_1_0", "", "")
	saml := client.GetSAMLAssertion(ticket)
	switch v := saml.(type) {
	case []byte:
		if !strings.Contains(string(v), ticket) {
			t.Errorf("Expected SAML assertion as bytes to contain ticket")
		}
	case string:
		if !strings.Contains(v, ticket) {
			t.Errorf("Expected SAML assertion string to contain ticket")
		}
	default:
		t.Errorf("Unknown type returned from GetSAMLAssertion")
	}
}

func TestV3CustomSession(t *testing.T) {
	client := cas.NewCASClientWithSession("3", "https://cas.example.com/cas/", "https://example.com/login", successResponse)
	user, attributes, pgtiou := client.VerifyTicket("ABC123")
	if user != "user@example.com" {
		t.Errorf("Expected user user@example.com, got %s", user)
	}
	if len(attributes) != 0 {
		t.Errorf("Expected no attributes for custom session")
	}
	if pgtiou != "" {
		t.Errorf("Expected empty pgtiou for custom session")
	}
}

func getClientV2() *cas.CASClientV2 {
	return cas.NewCASClientV2()
}

const successResponseWithJasig = `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>someuser</cas:user><cas:attributes><cas:attraStyle>Jasig</cas:attraStyle><cas:nombroj>unu</cas:nombroj><cas:nombroj>du</cas:nombroj><cas:nombroj>tri</cas:nombroj><cas:nombroj>kvar</cas:nombroj><cas:email>someuser@example.com</cas:email></cas:attributes></cas:authenticationSuccess></cas:serviceResponse>
`

func TestCAS2JasigAttributes(t *testing.T) {
	user, attributes, pgtiou := getClientV2().VerifyResponse(successResponseWithJasig)
	if user != "someuser" {
		t.Errorf("Expected user someuser, got %s", user)
	}
	expectedAttrs := map[string]interface{}{
		"email":   "someuser@example.com",
		"nombroj": []string{"unu", "du", "tri", "kvar"},
	}
	if attributes["email"] != expectedAttrs["email"] {
		t.Errorf("Expected 'email' to match, got %v", attributes["email"])
	}
	nombroj, ok := attributes["nombroj"].([]string)
	if !ok || len(nombroj) != 4 {
		t.Errorf("Expected nombroj to be string array len 4, got %v", attributes["nombroj"])
	}
	for i, val := range []string{"unu", "du", "tri", "kvar"} {
		if nombroj[i] != val {
			t.Errorf("Expected nombroj[%d]=%s, got %s", i, val, nombroj[i])
		}
	}
}

const successResponseWithNonStandardUser = `<?xml version="1.0" encoding="UTF-8"?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:utilisateur><cas:displayName>John Doe</cas:displayName><cas:user>someuser</cas:user><cas:uid>someuser</cas:uid></cas:utilisateur></cas:authenticationSuccess></cas:serviceResponse>
`

func TestCAS2NonStandardUserNode(t *testing.T) {
	user, _, _ := getClientV2().VerifyResponse(successResponseWithNonStandardUser)
	if user != "someuser" {
		t.Errorf("Expected user someuser, got %s", user)
	}
}

func TestUnsupportedProtocolVersion(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for unknown protocol version")
		}
	}()
	_ = cas.NewCASClient("unknown", "", "")
}

func TestVerifyLogoutRequestInvalidParameters(t *testing.T) {
	client := cas.NewCASClientWithSAMLV1()
	if client.VerifyLogoutRequest("", "") {
		t.Errorf("Expected false for blank logout params")
	}
}

func TestVerifyLogoutRequestSuccess(t *testing.T) {
	client := cas.NewCASClientWithSAMLV1()
	logoutRequest := `
<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
   ID="[RANDOM ID]" Version="2.0" IssueInstant="[CURRENT DATE/TIME]">
  <saml:NameID xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
    @NOT_USED@
  </saml:NameID>
  <samlp:SessionIndex>st-1234</samlp:SessionIndex>
</samlp:LogoutRequest>
    `
	ticket := "st-1234"
	if !client.VerifyLogoutRequest(logoutRequest, ticket) {
		t.Errorf("Expected true for matching session index in SAML logout request")
	}
}

func TestVerifyLogoutRequestInvalidST(t *testing.T) {
	client := cas.NewCASClientWithSAMLV1()
	logoutRequest := `
<samlp:LogoutRequest xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
   ID="[RANDOM ID]" Version="2.0" IssueInstant="[CURRENT DATE/TIME]">
  <saml:NameID xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
    @NOT_USED@
  </saml:NameID>
  <samlp:SessionIndex>st-1234</samlp:SessionIndex>
</samlp:LogoutRequest>
    `
	ticket := "st-not-match"
	if client.VerifyLogoutRequest(logoutRequest, ticket) {
		t.Errorf("Expected false for mismatched session index and ticket")
	}
}