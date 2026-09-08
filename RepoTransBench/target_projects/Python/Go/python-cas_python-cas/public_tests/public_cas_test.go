package public_tests

import (
	"strings"
	"testing"
	"casproject/cas"
)

func TestLoginURLHelperPublic(t *testing.T) {
	client := cas.NewCASClientBase(
		true, // renew
		nil,
		"https://cas.otherdomain.org/auth/",
		"https://anotherdomain.org/app/",
	)
	actual := client.GetLoginURL()
	expected := "https://cas.otherdomain.org/auth/login?service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F&renew=true"
	if actual != expected {
		t.Errorf("Expected login url %s, got %s", expected, actual)
	}
}

func TestLoginURLHelperWithExtraParamsPublic(t *testing.T) {
	client := cas.NewCASClientBase(
		false,
		map[string]string{"foo": "bar", "baz": "5678"},
		"https://cas.otherdomain.org/auth/",
		"https://anotherdomain.org/app/",
	)
	actual := client.GetLoginURL()
	if !strings.Contains(actual, "service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F") ||
		!strings.Contains(actual, "foo=bar") || !strings.Contains(actual, "baz=5678") {
		t.Errorf("Expected extra params and correct service in login url, got %s", actual)
	}
	if !strings.HasPrefix(actual, "https://cas.otherdomain.org/auth/login?") {
		t.Errorf("Login url did not start with expected prefix, got: %s", actual)
	}
}

func TestLoginURLHelperWithRenewPublic(t *testing.T) {
	client := cas.NewCASClientBase(
		true,
		nil,
		"https://cas.otherdomain.org/auth/",
		"https://anotherdomain.org/app/",
	)
	actual := client.GetLoginURL()
	if !strings.Contains(actual, "renew=true") ||
		!strings.Contains(actual, "service=https%3A%2F%2Fanotherdomain.org%2Fapp%2F") {
		t.Errorf("Expected renew/service params in login url: %s", actual)
	}
}

func getLogoutClientV1Public() *cas.CASClient {
	return cas.NewCASClient("1", "https://cas.logouttest.org/sso/", "")
}

func getLogoutClientV2Public() *cas.CASClient {
	return cas.NewCASClient("2", "https://cas.logouttest.org/sso/", "")
}

func getLogoutClientV3Public() *cas.CASClient {
	return cas.NewCASClient("3", "https://cas.logouttest.org/sso/", "")
}

func TestLogoutURLPublic(t *testing.T) {
	client := getLogoutClientV3Public()
	actual := client.GetLogoutURL("")
	expected := "https://cas.logouttest.org/sso/logout"
	if actual != expected {
		t.Errorf("Expected public logout url %s, got %s", expected, actual)
	}
}

func TestV1LogoutURLWithRedirectPublic(t *testing.T) {
	client := getLogoutClientV1Public()
	actual := client.GetLogoutURL("https://anotherdomain.org/goodbye/")
	expected := "https://cas.logouttest.org/sso/logout?url=https%3A%2F%2Fanotherdomain.org%2Fgoodbye%2F"
	if actual != expected {
		t.Errorf("Expected v1 logout with redirect %s, got %s", expected, actual)
	}
}

func TestV2LogoutURLWithRedirectPublic(t *testing.T) {
	client := getLogoutClientV2Public()
	actual := client.GetLogoutURL("https://anotherdomain.org/goodbye/")
	expected := "https://cas.logouttest.org/sso/logout?url=https%3A%2F%2Fanotherdomain.org%2Fgoodbye%2F"
	if actual != expected {
		t.Errorf("Expected v2 logout with redirect %s, got %s", expected, actual)
	}
}

func TestV3LogoutURLWithRedirectPublic(t *testing.T) {
	client := getLogoutClientV3Public()
	actual := client.GetLogoutURL("https://anotherdomain.org/goodbye/")
	expected := "https://cas.logouttest.org/sso/logout?service=https%3A%2F%2Fanotherdomain.org%2Fgoodbye%2F"
	if actual != expected {
		t.Errorf("Expected v3 logout with redirect %s, got %s", expected, actual)
	}
}

func TestV3LogoutURLWithoutRedirectPublic(t *testing.T) {
	client := getLogoutClientV3Public()
	actual := client.GetLogoutURL("")
	expected := "https://cas.logouttest.org/sso/logout"
	if actual != expected {
		t.Errorf("Expected v3 logout no redirect %s, got %s", expected, actual)
	}
}

// --- Success/failure responses

func getClientV3Public() *cas.CASClient {
	return cas.NewCASClient("3", "https://cas.mysite.org/sso/", "https://mysite.org/home")
}

const successResponsePublic = ` + "`" + `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>public_user@domain.org</cas:user></cas:authenticationSuccess></cas:serviceResponse>
` + "`" + `

func TestCAS3BasicSuccessfulResponseVerificationPublic(t *testing.T) {
	user, attributes, pgtiou := getClientV3Public().VerifyResponse(successResponsePublic)
	if user != "public_user@domain.org" {
		t.Errorf("Expected public_user@domain.org user, got %v", user)
	}
	if len(attributes) > 0 {
		t.Errorf("Expected no attributes, got %v", attributes)
	}
	if pgtiou != "" {
		t.Errorf("Expected no pgtiou, got %v", pgtiou)
	}
}

const successResponseWithAttributesPublic = ` + "`" + `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>public_user@domain.org</cas:user><cas:attributes><cas:alpha>xyz</cas:alpha><cas:beta>9999</cas:beta></cas:attributes></cas:authenticationSuccess></cas:serviceResponse>
` + "`" + `
func TestCAS3SuccessfulResponseVerificationWithAttributesPublic(t *testing.T) {
	user, attributes, pgtiou := getClientV3Public().VerifyResponse(successResponseWithAttributesPublic)
	if user != "public_user@domain.org" {
		t.Errorf("Expected public_user@domain.org, got %v", user)
	}
	if pgtiou != "" {
		t.Errorf("Expected no pgtiou, got %v", pgtiou)
	}
	if attributes["alpha"] != "xyz" || attributes["beta"] != "9999" {
		t.Errorf("Expected alpha=xyz and beta=9999 in attributes, got %v", attributes)
	}
}

const successResponseWithPGTIOUPublic = ` + "`" + `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationSuccess><cas:user>public_user@domain.org</cas:user><cas:proxyGrantingTicket>PGTIOU-54321-aaaa</cas:proxyGrantingTicket></cas:authenticationSuccess></cas:serviceResponse>
` + "`" + `
func TestSuccessfulResponseVerificationWithPGTIOUPublic(t *testing.T) {
	user, _, pgtiou := getClientV3Public().VerifyResponse(successResponseWithPGTIOUPublic)
	if user != "public_user@domain.org" {
		t.Errorf("Expected public_user@domain.org, got %v", user)
	}
	if pgtiou != "PGTIOU-54321-aaaa" {
		t.Errorf("Expected PGTIOU-54321-aaaa, got %v", pgtiou)
	}
}

const failureResponsePublic = ` + "`" + `<?xml version='1.0' encoding='UTF-8'?>
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas"><cas:authenticationFailure code="INVALID_TICKET">service ticket ST-555-ERRTEST has been revoked</cas:authenticationFailure></cas:serviceResponse>
` + "`" + `
func TestUnsuccessfulResponsePublic(t *testing.T) {
	user, attributes, pgtiou := getClientV3Public().VerifyResponse(failureResponsePublic)
	if user != "" {
		t.Errorf("Expected user to be empty in unsuccessful response")
	}
	if pgtiou != "" {
		t.Errorf("Expected no pgtiou in unsuccessful response")
	}
	if len(attributes) != 0 {
		t.Errorf("Expected attributes to be empty for unsuccessful, got %v", attributes)
	}
}

func TestProxyURLPublic(t *testing.T) {
	client := getClientV3Public()
	tgt := "tgt-PUBLIC-5678"
	proxyUrl := client.GetProxyURL(tgt)
	expectedBase := "https://cas.mysite.org/sso/proxy?"
	if !strings.HasPrefix(proxyUrl, expectedBase) {
		t.Errorf("Expected proxy url to start with %s, got %s", expectedBase, proxyUrl)
	}
	if !strings.Contains(proxyUrl, "pgt="+tgt) {
		t.Errorf("Expected proxy url to contain pgt param")
	}
	if !strings.Contains(proxyUrl, "targetService=https%3A%2F%2Fmysite.org%2Fhome") {
		t.Errorf("Expected proxy url to contain targetService param")
	}
}