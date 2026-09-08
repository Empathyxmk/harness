package original

import (
	"springatticsso/tests/testutil"
	"testing"
)

func TestDashboardMessage(t *testing.T) {
	app := testutil.NewSsoApplication()
	message := app.Dashboard()
	if message == nil {
		t.Fatal("Dashboard() returned nil")
	}
	msg, ok := message["message"]
	if !ok {
		t.Error(`Expected key "message" in dashboard map`)
	}
	if msg != "Yay!" {
		t.Errorf(`Expected message value "Yay!", got %v`, msg)
	}
}

func TestUserPrincipal(t *testing.T) {
	app := testutil.NewSsoApplication()
	p := testutil.PrincipalFunc(func() string { return "testuser" })
	ret := app.User(p)
	if ret != p {
		t.Error("Returned principal does not match input principal")
	}
	if ret.GetName() != "testuser" {
		t.Errorf("Expected user name 'testuser', got '%s'", ret.GetName())
	}
}

func TestMainNoArgs(t *testing.T) {
	// Just for coverage
	testutil.SsoMain([]string{})
}

func TestLoginErrorsDashboard(t *testing.T) {
	errors := testutil.NewLoginErrors()
	path := errors.Dashboard()
	if path != "redirect:/#/" {
		t.Errorf("Expected 'redirect:/#/', got '%s'", path)
	}
}

func TestCsrfHeaderFilterSetsCookie(t *testing.T) {
	config := testutil.NewLoginConfigurer()
	req := &testutil.MockRequest{}
	resp := &testutil.MockResponse{}
	csrf := &testutil.MockCsrfToken{Token: "testToken"}
	req.SetAttribute("CsrfToken", csrf)
	chain := &testutil.MockChain{}

	filter := config.CsrfHeaderFilter()

	err := filter.DoFilter(req, resp, chain)
	if err != nil {
		t.Errorf("DoFilter() error = %v", err)
	}
	if len(resp.AddedCookies) != 1 {
		t.Error("Expected 1 cookie to be added")
	}
	ok := false
	for _, c := range resp.AddedCookies {
		if c.Name == "XSRF-TOKEN" && c.Value == "testToken" {
			ok = true
		}
	}
	if !ok {
		t.Error("Expected XSRF-TOKEN cookie with correct value")
	}
	if !chain.Called {
		t.Error("Expected chain.DoFilter to be called")
	}
}

func TestCsrfHeaderFilterNoCsrf(t *testing.T) {
	config := testutil.NewLoginConfigurer()
	req := &testutil.MockRequest{}
	resp := &testutil.MockResponse{}
	chain := &testutil.MockChain{}
	// No CSRF token set

	filter := config.CsrfHeaderFilter()
	err := filter.DoFilter(req, resp, chain)
	if err != nil {
		t.Errorf("DoFilter() error = %v", err)
	}
	if len(resp.AddedCookies) != 0 {
		t.Error("Expected no cookies to be added")
	}
	if !chain.Called {
		t.Error("Expected chain.DoFilter to be called")
	}
}

func TestCsrfTokenRepository(t *testing.T) {
	config := testutil.NewLoginConfigurer()
	repo := config.CsrfTokenRepository()
	if repo.HeaderName != "X-XSRF-TOKEN" {
		t.Errorf("Expected HeaderName to be 'X-XSRF-TOKEN', got '%s'", repo.HeaderName)
	}
}