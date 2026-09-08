package public_tests

import (
	"strings"
	"testing"

	"github.com/example/flasklogin/src"
)

func TestInstanceDefaultsPublic(t *testing.T) {
	lm := src.NewLoginManager()
	if lm.AnonymousUser == nil {
		t.Errorf("AnonymousUser missing on LoginManager")
	}
	// "callable"
	// In Go, functions or nil indicate "callable"; already checked.
	if lm.LoginView != nil {
		t.Errorf("LoginView should be nil by default")
	}
	if lm.BlueprintLoginViews == nil {
		t.Errorf("BlueprintLoginViews should be a map")
	}
	if !strings.Contains(lm.LoginMessageCategory, "message") {
		t.Errorf("LoginMessageCategory should contain 'message'")
	}
	if !strings.Contains(strings.ToLower(lm.NeedsRefreshMessage), "refresh") {
		t.Errorf("NeedsRefreshMessage should contain 'refresh'")
	}
	if lm.IDAttribute != "get_id" {
		t.Errorf("IDAttribute should be 'get_id'")
	}
	switch lm.SessionProtection.(type) {
	case string:
		if lm.SessionProtection != "basic" && lm.SessionProtection != "strong" && lm.SessionProtection != nil {
			t.Errorf("SessionProtection invalid")
		}
	case nil:
		// ok
	}
}

func TestLoginManagerCustomValuesPublic(t *testing.T) {
	lm := src.NewLoginManager()
	val := "/custom_login"
	lm.LoginView = &val
	val2 := "/refresh_needed"
	lm.RefreshView = &val2
	lm.LoginMessage = "You must sign in!"
	lm.BlueprintLoginViews["bp2"] = "/bp2_custom_login"
	if lm.LoginView == nil || !strings.HasPrefix(*lm.LoginView, "/") {
		t.Errorf("LoginView not set correctly")
	}
	if lm.RefreshView == nil || !strings.HasSuffix(*lm.RefreshView, "needed") {
		t.Errorf("RefreshView not set correctly")
	}
	if !strings.Contains(lm.LoginMessage, "sign in") {
		t.Errorf("LoginMessage not set")
	}
	if _, ok := lm.BlueprintLoginViews["bp2"]; !ok || !strings.HasPrefix(lm.BlueprintLoginViews["bp2"], "/bp2") {
		t.Errorf("bp2 not set correctly")
	}
	lm.SessionProtection = "strong"
	if lm.SessionProtection != "strong" {
		t.Errorf("SessionProtection not set to strong")
	}
}

func TestLoginManagerAnonymousUserPublic(t *testing.T) {
	lm := src.NewLoginManager()
	type CustomAnon struct{}
	lm.AnonymousUser = CustomAnon{}
	_, ok := lm.AnonymousUser.(CustomAnon)
	if !ok {
		t.Errorf("AnonymousUser not settable")
	}
}

func TestLocalizeCallbackPublic(t *testing.T) {
	lm := src.NewLoginManager()
	called := ""
	fakeLocalizer := func(txt string) { called = txt }
	lm.LocalizeCallback = fakeLocalizer
	lm.LocalizeCallback("hello")
	if called != "hello" {
		t.Errorf("LocalizeCallback did not set value")
	}
}