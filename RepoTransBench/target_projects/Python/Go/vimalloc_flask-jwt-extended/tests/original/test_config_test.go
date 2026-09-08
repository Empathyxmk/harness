package original

import (
	"testing"
	"github.com/example/vimalloc_flask_jwt_extended_go/tests"
)

func TestConfigStructFields(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey:     "abcde12345",
		TokenLocation: "headers",
		JWTCookieName: "jwt_token_cookie",
		JWTHeaderName: "Authorization",
		JWTHeaderType: "Bearer",
	}
	app := tests.NewTestJWTApp(config)

	if app.Config.SecretKey != "abcde12345" {
		t.Errorf("Expected SecretKey 'abcde12345', got '%s'", app.Config.SecretKey)
	}
	if app.Config.TokenLocation != "headers" {
		t.Errorf("Expected TokenLocation 'headers', got '%s'", app.Config.TokenLocation)
	}
	if app.Config.JWTCookieName != "jwt_token_cookie" {
		t.Errorf("Expected JWTCookieName 'jwt_token_cookie', got '%s'", app.Config.JWTCookieName)
	}
	if app.Config.JWTHeaderName != "Authorization" {
		t.Errorf("Expected JWTHeaderName 'Authorization', got '%s'", app.Config.JWTHeaderName)
	}
	if app.Config.JWTHeaderType != "Bearer" {
		t.Errorf("Expected JWTHeaderType 'Bearer', got '%s'", app.Config.JWTHeaderType)
	}
}

func TestConfigDefaultValues(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey: "default-secret",
	}
	app := tests.NewTestJWTApp(config)

	if app.Config.SecretKey != "default-secret" {
		t.Errorf("Expected SecretKey 'default-secret', got '%s'", app.Config.SecretKey)
	}
}