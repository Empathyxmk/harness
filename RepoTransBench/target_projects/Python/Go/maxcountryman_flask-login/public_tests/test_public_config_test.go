package public_tests

import (
	"strings"
	"testing"

	"github.com/example/flasklogin/src"
)

func TestCookieNamePublic(t *testing.T) {
	if !strings.HasPrefix(src.COOKIE_NAME, "remember") {
		t.Errorf("COOKIE_NAME does not start with remember")
	}
}

func TestCookieDurationPublic(t *testing.T) {
	// Check days >= 300
	if src.COOKIE_DURATION.Hours()/24 < 300 {
		t.Errorf("COOKIE_DURATION should be at least 300 days")
	}
}

func TestCookieSecurePublic(t *testing.T) {
	if src.COOKIE_SECURE != false {
		t.Errorf("COOKIE_SECURE should be false")
	}
}

func TestCookieHTTPOnlyPublic(t *testing.T) {
	if src.COOKIE_HTTPONLY != true {
		t.Errorf("COOKIE_HTTPONLY should be true")
	}
}

func TestCookieSameSitePublic(t *testing.T) {
	if src.COOKIE_SAMESITE != nil {
		t.Errorf("COOKIE_SAMESITE should be nil")
	}
}

func TestLoginMessagePublic(t *testing.T) {
	if !strings.Contains(strings.ToLower(src.LOGIN_MESSAGE), "log in") {
		t.Errorf("LOGIN_MESSAGE should contain 'log in'")
	}
}

func TestLoginMessageCategoryPublic(t *testing.T) {
	if len(src.LOGIN_MESSAGE_CATEGORY) <= 2 {
		t.Errorf("LOGIN_MESSAGE_CATEGORY too short")
	}
}

func TestRefreshMessagePublic(t *testing.T) {
	if !strings.HasPrefix(src.REFRESH_MESSAGE, "Please reauth") {
		t.Errorf("REFRESH_MESSAGE should start with 'Please reauth'")
	}
}

func TestRefreshMessageCategoryPublic(t *testing.T) {
	if src.REFRESH_MESSAGE_CATEGORY != src.LOGIN_MESSAGE_CATEGORY {
		t.Errorf("REFRESH_MESSAGE_CATEGORY != LOGIN_MESSAGE_CATEGORY")
	}
}

func TestIDAttributePublic(t *testing.T) {
	if !strings.HasSuffix(src.ID_ATTRIBUTE, "id") {
		t.Errorf("ID_ATTRIBUTE should end with 'id'")
	}
}

func TestSessionKeysPublic(t *testing.T) {
	foundUserID, foundID := false, false
	for _, k := range src.SESSION_KEYS {
		if k == "_user_id" {
			foundUserID = true
		}
		if k == "_id" {
			foundID = true
		}
	}
	if !foundUserID || !foundID {
		t.Errorf("SESSION_KEYS missing user_id or _id")
	}
}

func TestExemptMethodsPublic(t *testing.T) {
	if _, ok := src.EXEMPT_METHODS["OPTIONS"]; !ok {
		t.Errorf("EXEMPT_METHODS missing OPTIONS")
	}
}

func TestUseSessionForNextPublic(t *testing.T) {
	if src.USE_SESSION_FOR_NEXT != false {
		t.Errorf("USE_SESSION_FOR_NEXT should be false")
	}
}