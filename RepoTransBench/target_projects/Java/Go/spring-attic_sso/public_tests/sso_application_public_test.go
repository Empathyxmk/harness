package public_tests

import (
	"springatticsso/tests/testutil"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestDashboardMessagePublic(t *testing.T) {
	app := testutil.NewSsoApplication()
	msg := app.Dashboard()
	assert.NotNil(t, msg)
	val, ok := msg["message"]
	assert.True(t, ok, "expected 'message' key")
	assert.IsType(t, "", val)
}

func TestUserPrincipalPublic(t *testing.T) {
	app := testutil.NewSsoApplication()
	// "publicuser"
	p := testutil.PrincipalFunc(func() string { return "publicuser" })
	ret := app.User(p)
	assert.Equal(t, p, ret)
	assert.Equal(t, "publicuser", ret.GetName())

	// Unicode username
	specialP := testutil.PrincipalFunc(func() string { return "用户123" })
	specialRet := app.User(specialP)
	assert.Equal(t, "用户123", specialRet.GetName())
}

func TestMainWithArgsPublic(t *testing.T) {
	testutil.SsoMain([]string{"--fakeArg=1"})
}

func TestLoginErrorsDashboardPublic(t *testing.T) {
	errors := testutil.NewLoginErrors()
	result := errors.Dashboard()
	assert.True(t, len(result) >= 1)
	assert.True(t, len(result) > 0 && result[0:9] == "redirect:/")
	assert.Contains(t, result, "/")
	assert.Equal(t, "redirect:/#/", result)
}

func TestCsrfHeaderFilterSetsCookiePublic(t *testing.T) {
	config := testutil.NewLoginConfigurer()
	req := &testutil.MockRequest{}
	resp := &testutil.MockResponse{}
	csrf := &testutil.MockCsrfToken{Token: "publicTokenXYZ"}
	req.SetAttribute("CsrfToken", csrf)
	chain := &testutil.MockChain{}

	filter := config.CsrfHeaderFilter()
	err := filter.DoFilter(req, resp, chain)
	assert.NoError(t, err)
	added := false
	for _, c := range resp.AddedCookies {
		if c.Name == "XSRF-TOKEN" && c.Value == "publicTokenXYZ" {
			added = true
		}
	}
	assert.True(t, added, "Expected cookie with name XSRF-TOKEN and value publicTokenXYZ")
	assert.True(t, chain.Called, "DoFilter on chain should be called")
}

func TestCsrfHeaderFilterNoCsrfPublic(t *testing.T) {
	config := testutil.NewLoginConfigurer()
	req := &testutil.MockRequest{}
	resp := &testutil.MockResponse{}
	chain := &testutil.MockChain{}

	filter := config.CsrfHeaderFilter()
	err := filter.DoFilter(req, resp, chain)
	assert.NoError(t, err)
	assert.Len(t, resp.AddedCookies, 0, "No cookies should be added")
	assert.True(t, chain.Called, "DoFilter on chain should be called")
}

func TestCsrfTokenRepositoryPublic(t *testing.T) {
	config := testutil.NewLoginConfigurer()
	repo := config.CsrfTokenRepository()
	assert.NotNil(t, repo)
	assert.IsType(t, "", repo.HeaderName)
	assert.Equal(t, "X-XSRF-TOKEN", repo.HeaderName)
}