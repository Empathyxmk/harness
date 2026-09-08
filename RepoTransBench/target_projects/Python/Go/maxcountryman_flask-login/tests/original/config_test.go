package original

import (
	"strings"
	"testing"

	"github.com/example/flasklogin/src"
)

func TestConfigValues(t *testing.T) {
	if src.COOKIE_NAME != "remember_token" {
		t.Errorf("COOKIE_NAME incorrect")
	}
	if src.COOKIE_DURATION.Hours()/24 != 365 {
		t.Errorf("COOKIE_DURATION days not 365")
	}
	if src.COOKIE_SECURE != false {
		t.Errorf("COOKIE_SECURE should be false")
	}
	if src.COOKIE_HTTPONLY != true {
		t.Errorf("COOKIE_HTTPONLY should be true")
	}
	_, ok := src.EXEMPT_METHODS["OPTIONS"]
	if !ok {
		t.Errorf("EXEMPT_METHODS should contain OPTIONS")
	}
	if src.LOGIN_MESSAGE != "Please log in to access this page." {
		t.Errorf("LOGIN_MESSAGE incorrect")
	}
	if src.LOGIN_MESSAGE_CATEGORY != "message" {
		t.Errorf("LOGIN_MESSAGE_CATEGORY should be 'message'")
	}
	if !strings.HasPrefix(src.REFRESH_MESSAGE, "Please reauthenticate") {
		t.Errorf("REFRESH_MESSAGE incorrect")
	}
	if src.REFRESH_MESSAGE_CATEGORY != "message" {
		t.Errorf("REFRESH_MESSAGE_CATEGORY should be 'message'")
	}
	if src.ID_ATTRIBUTE != "get_id" {
		t.Errorf("ID_ATTRIBUTE should be 'get_id'")
	}
	foundUserID := false
	foundRemember := false
	for _, v := range src.SESSION_KEYS {
		if v == "_user_id" {
			foundUserID = true
		}
		if v == "_remember" {
			foundRemember = true
		}
	}
	if !foundUserID {
		t.Errorf("SESSION_KEYS should contain _user_id")
	}
	if !foundRemember {
		t.Errorf("SESSION_KEYS should contain _remember")
	}
	if src.USE_SESSION_FOR_NEXT != false {
		t.Errorf("USE_SESSION_FOR_NEXT should be false")
	}
}