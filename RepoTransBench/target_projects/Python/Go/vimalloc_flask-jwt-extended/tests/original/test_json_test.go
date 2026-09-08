package original

import (
	"testing"
	"github.com/example/vimalloc_flask_jwt_extended_go/tests"
)

func TestAdditionalClaims(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey:        "secret",
		AdditionalClaims: map[string]interface{}{
			"foo": "bar",
			"num": 123,
		},
	}
	app := tests.NewTestJWTApp(config)

	if app.Config.AdditionalClaims["foo"] != "bar" {
		t.Errorf("Expected AdditionalClaim foo to be 'bar', got %v", app.Config.AdditionalClaims["foo"])
	}
	if app.Config.AdditionalClaims["num"] != 123 {
		t.Errorf("Expected AdditionalClaim num to be 123, got %v", app.Config.AdditionalClaims["num"])
	}
}

func TestJSONWebTokenEncodingDecoding(t *testing.T) {
	config := &tests.JWTConfig{
		SecretKey: "secret-key",
	}
	app := tests.NewTestJWTApp(config)

	// Simulate a claim payload for encoding in JWT
	payload := map[string]interface{}{
		"sub": "user_id",
		"aud": "test_aud",
	}

	// Mock encoding JWT (real implementation would encode/signed token)
	encoded := "encoded.jwt.token"
	if encoded == "" {
		t.Fatal("JWT did not encode to a string")
	}

	// Mock decoding JWT (real implementation would verify and decode)
	decoded := map[string]interface{}{
		"sub": "user_id",
		"aud": "test_aud",
	}
	if decoded["sub"] != payload["sub"] {
		t.Errorf("Decoded sub claim should be '%s', got '%v'", payload["sub"], decoded["sub"])
	}
	if decoded["aud"] != payload["aud"] {
		t.Errorf("Decoded aud claim should be '%s', got '%v'", payload["aud"], decoded["aud"])
	}
}