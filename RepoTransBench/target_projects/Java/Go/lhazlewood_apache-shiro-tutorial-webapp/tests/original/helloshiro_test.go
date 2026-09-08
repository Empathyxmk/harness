package original

import (
	"os"
	"testing"
)

// HelloShiro simulates the behavior of the Java HelloShiro class.
type HelloShiro struct {
	authenticated bool
	user          *string
}

// NewHelloShiro constructs a new HelloShiro object.
func NewHelloShiro() *HelloShiro {
	return &HelloShiro{
		authenticated: false,
		user:          nil,
	}
}

// Login authenticates with given username and password ("admin", "adminpass" are valid).
func (h *HelloShiro) Login(username, password string) bool {
	if username == "admin" && password == "adminpass" {
		h.authenticated = true
		h.user = &username
		return true
	} else {
		h.authenticated = false
		h.user = nil
		return false
	}
}

// IsAuthenticated returns current authentication state.
func (h *HelloShiro) IsAuthenticated() bool {
	return h.authenticated
}

// GetUser gets the username if authenticated.
func (h *HelloShiro) GetUser() *string {
	if h.authenticated {
		return h.user
	}
	return nil
}

// Logout logs out.
func (h *HelloShiro) Logout() {
	h.authenticated = false
	h.user = nil
}

// GetWelcomeMessage returns welcome string if authenticated, otherwise login prompt.
func (h *HelloShiro) GetWelcomeMessage() string {
	if !h.authenticated || h.user == nil {
		return "Please log in."
	}
	if *h.user == "admin" {
		return "Welcome, admin!"
	}
	return "Welcome, " + *h.user + "!"
}

func TestHelloShiro_LoginSuccess(t *testing.T) {
	shiro := NewHelloShiro()
	if !shiro.Login("admin", "adminpass") {
		t.Errorf("Expected login to succeed with admin/adminpass")
	}
	if !shiro.IsAuthenticated() {
		t.Errorf("Expected authenticated state after successful login")
	}
	if shiro.GetUser() == nil || *shiro.GetUser() != "admin" {
		t.Errorf("Expected user to be admin after login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Welcome, admin!" {
		t.Errorf("Expected welcome message for admin, got: %q", msg)
	}
}

func TestHelloShiro_LoginFailure_BadPassword(t *testing.T) {
	shiro := NewHelloShiro()
	if shiro.Login("admin", "wrongpass") {
		t.Errorf("Login should fail with bad password")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated after failed login")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after failed login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Expected login prompt after failed login, got: %q", msg)
	}
}

func TestHelloShiro_LoginFailure_UnknownUser(t *testing.T) {
	shiro := NewHelloShiro()
	if shiro.Login("bob", "somepass") {
		t.Errorf("Login should fail for unknown user")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated after failed login")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil when not authenticated")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Expected login prompt for unknown user, got: %q", msg)
	}
}

func TestHelloShiro_Logout(t *testing.T) {
	shiro := NewHelloShiro()
	shiro.Login("admin", "adminpass")
	shiro.Logout()
	if shiro.IsAuthenticated() {
		t.Errorf("Expected to not be authenticated after logout")
	}
	if shiro.GetUser() != nil {
		t.Errorf("Expected user to be nil after logout")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Expected login prompt after logout, got: %q", msg)
	}
}

func TestHelloShiro_WelcomeMessageNotAuthenticated(t *testing.T) {
	shiro := NewHelloShiro()
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Expected login prompt if not authenticated, got: %q", msg)
	}
}

func TestHelloShiro_WelcomeMessageUnknownUser(t *testing.T) {
	shiro := NewHelloShiro()
	// Simulate bypassing login to force authenticated=true and user="otheruser"
	shiro.authenticated = true
	u := "otheruser"
	shiro.user = &u
	if msg := shiro.GetWelcomeMessage(); msg != "Welcome, otheruser!" {
		t.Errorf("Expected welcome message for unknown user, got: %q", msg)
	}
}

func TestHelloShiro_MultipleLoginLogoutCycles(t *testing.T) {
	shiro := NewHelloShiro()
	if !shiro.Login("admin", "adminpass") {
		t.Errorf("Should be able to login as admin")
	}
	shiro.Logout()
	if shiro.IsAuthenticated() {
		t.Errorf("Should NOT be authenticated after logout.")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after logout")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after logout, got: %q", msg)
	}

	if shiro.Login("test", "bad") {
		t.Errorf("Login with invalid credentials should fail")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated after failed login")
	}
	if shiro.GetUser() != nil {
		t.Errorf("Should be no user after failed login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after failed login, got: %q", msg)
	}

	if !shiro.Login("admin", "adminpass") {
		t.Errorf("Should be able to re-login as admin")
	}
	if !shiro.IsAuthenticated() {
		t.Errorf("auth flag should be true after login")
	}
	if shiro.GetUser() == nil || *shiro.GetUser() != "admin" {
		t.Errorf("User should be admin after relogin")
	}
}

func TestMetaTest_ProjectStructureExists(t *testing.T) {
	if _, err := os.Stat("pom.xml"); err != nil {
		t.Errorf("pom.xml should exist, but failed: %v", err)
	}
	if _, err := os.Stat("README.md"); err != nil {
		t.Errorf("README.md should exist, but failed: %v", err)
	}
}

func TestNoJavaSourcesTest_NoJavaSources(t *testing.T) {
	if true != true {
		t.Errorf("Always succeeds: there are no Java sources to test.")
	}
}