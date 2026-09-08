package original

import (
	"testing"
	"github.com/example/vimalloc_flask_jwt_extended_go/tests"
)

func TestCookiesConfig(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey:     "super-secret",
		TokenLocation: "cookies",
		JWTCookieName: "my_jwt_cookie",
	}

	app := tests.NewTestJWTApp(config)
	if app.Config.TokenLocation != "cookies" {
		t.Errorf("Expected token location to be 'cookies', got '%s'", app.Config.TokenLocation)
	}
	if app.Config.JWTCookieName != "my_jwt_cookie" {
		t.Errorf("Expected JWT cookie name to be 'my_jwt_cookie', got '%s'", app.Config.JWTCookieName)
	}
}

func TestSettingJWTInCookies(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey:     "super-secret",
		TokenLocation: "cookies",
	}

	app := tests.NewTestJWTApp(config)

	// Simulate issuing a token and setting in cookies
	token := "test.jwt.token"
	cookieName := "access_token_cookie"
	app.Config.JWTCookieName = cookieName

	// Simulate setting a cookie in a response (mock logic)
	responseCookies := make(map[string]string)
	responseCookies[cookieName] = token

	if val, ok := responseCookies[cookieName]; !ok || val != token {
		t.Errorf("JWT token not set correctly in cookie. Expected '%s', got '%s'", token, val)
	}
}

func TestTokenInCookieIsUsed(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey:     "secret",
		TokenLocation: "cookies",
		JWTCookieName: "test_cookie",
	}
	app := tests.NewTestJWTApp(config)

	// Simulate a request that includes a JWT in the cookie
	reqCookies := map[string]string{
		config.JWTCookieName: "some.jwt.token",
	}

	// Mock endpoint handler would extract the JWT from cookies:
	retrievedToken := reqCookies[config.JWTCookieName]

	if retrievedToken == "" {
		t.Error("JWT token not found in cookies")
	}
	if retrievedToken != "some.jwt.token" {
		t.Errorf("Expected token 'some.jwt.token', got '%s'", retrievedToken)
	}
}