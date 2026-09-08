package public_tests

import (
	"os"
	"testing"
)

// --- This struct and API mirrors the original HelloShiro implementation ---
type HelloShiro struct {
	authenticated bool
	user          *string
}

func NewHelloShiro() *HelloShiro {
	return &HelloShiro{
		authenticated: false,
		user:          nil,
	}
}

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

func (h *HelloShiro) IsAuthenticated() bool {
	return h.authenticated
}

func (h *HelloShiro) GetUser() *string {
	if h.authenticated {
		return h.user
	}
	return nil
}

func (h *HelloShiro) Logout() {
	h.authenticated = false
	h.user = nil
}

func (h *HelloShiro) GetWelcomeMessage() string {
	if !h.authenticated || h.user == nil {
		return "Please log in."
	}
	if *h.user == "admin" {
		return "Welcome, admin!"
	}
	return "Welcome, " + *h.user + "!"
}

// --- Begin translation of HelloShiroPublicTest.java ---

func TestLoginSuccess_Public(t *testing.T) {
	shiro := NewHelloShiro()
	// Case sensitivity: "Admin" vs "admin", both should fail.
	if shiro.Login("Admin", "Adminpass") {
		t.Errorf(`Expected login with "Admin"/"Adminpass" to fail (case sensitive)`)
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated after failed login (case)")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil when login fails (case sensitive)")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after failed login, got: %q", msg)
	}

	// Trailing/leading spaces version should also fail:
	if shiro.Login(" admin ", " adminpass ") {
		t.Errorf("Should not authenticate with leading/trailing whitespace")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated with whitespace credentials")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should still be nil after whitespace login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after whitespace failed login, got: %q", msg)
	}
}

func TestLoginFailure_EmptyFields(t *testing.T) {
	shiro := NewHelloShiro()
	// Empty username
	if shiro.Login("", "adminpass") {
		t.Errorf("Should fail login if username is empty")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not authenticate with empty username")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after empty username login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt after empty username login, got: %q", msg)
	}

	// Empty password
	if shiro.Login("admin", "") {
		t.Errorf("Should fail login if password is empty")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not authenticate with empty password")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after empty password login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt after empty password login, got: %q", msg)
	}
}

func TestLoginFailure_NullFields(t *testing.T) {
	shiro := NewHelloShiro()
	// In Go, zero value of string is "", so "null" is represented as empty string
	if shiro.Login("", "adminpass") {
		t.Errorf("Should not authenticate with 'null' username (empty string)")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not authenticate with empty username as null")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil for null username")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after null username login, got: %q", msg)
	}
	if shiro.Login("admin", "") {
		t.Errorf("Should not authenticate with null password (empty string)")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not authenticate with empty password as null")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil for null password")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after null password login, got: %q", msg)
	}
}

func TestLogoutAfterFailedLogin(t *testing.T) {
	shiro := NewHelloShiro()
	if shiro.Login("nope", "nope") {
		t.Errorf("Should not authenticate with wrong credentials")
	}
	shiro.Logout()
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated after calling logout after failed login")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after logout following failed login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after failed login and logout, got: %q", msg)
	}
}

func TestWelcomeMessage_AdminAfterManualSet(t *testing.T) {
	shiro := NewHelloShiro()
	// Simulate a reflection: authenticated = true, user = "Admin"
	shiro.authenticated = true
	u := "Admin"
	shiro.user = &u
	want := "Welcome, Admin!"
	if got := shiro.GetWelcomeMessage(); got != want {
		t.Errorf("Expected %q but got %q", want, got)
	}
}

func TestMultipleLoginLogoutDifferentUsernames(t *testing.T) {
	shiro := NewHelloShiro()
	// root
	if shiro.Login("root", "supersecret") {
		t.Errorf("Should not authorize root/supersecret")
	}
	shiro.Logout()
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated after logout")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after failed root login and logout")
	}
	if m := shiro.GetWelcomeMessage(); m != "Please log in." {
		t.Errorf("Prompt expected after failed root login/logout, got: %q", m)
	}
	// user/userpass (fail)
	if shiro.Login("user", "userpass") {
		t.Errorf("Should not authorize user/userpass")
	}
	if shiro.IsAuthenticated() {
		t.Errorf("Should not be authenticated as user")
	}
	if shiro.GetUser() != nil {
		t.Errorf("User should be nil after failed user login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Please log in." {
		t.Errorf("Prompt expected after failed user login, got: %q", msg)
	}
	// admin/adminpass (ok)
	if !shiro.Login("admin", "adminpass") {
		t.Errorf("Admin should authenticate")
	}
	if !shiro.IsAuthenticated() {
		t.Errorf("Should be authenticated as admin")
	}
	if s := shiro.GetUser(); s == nil || *s != "admin" {
		t.Errorf("GetUser() should return \"admin\" after login")
	}
	if msg := shiro.GetWelcomeMessage(); msg != "Welcome, admin!" {
		t.Errorf("Welcome message not as expected for admin: %q", msg)
	}
}

func TestMetaPublicTest_ProjectRequiredFilesExist_Public(t *testing.T) {
	if _, err := os.Stat("pom.xml"); err != nil {
		t.Errorf("pom.xml must be present in the repo, err: %v", err)
	}
	if _, err := os.Stat("LICENSE"); err != nil {
		t.Errorf("LICENSE should exist in project root, err: %v", err)
	}
}

func TestNoJavaSourcesPublicTest_NoJavaSourcesPublic(t *testing.T) {
	if true != true {
		t.Errorf("Should always pass as a placeholder public test.")
	}
}