package public_tests

import (
	"TypeError_secure/secure"
	"testing"
)

type PublicMockResponse struct {
	Headers map[string]string
}

func (p *PublicMockResponse) SetHeader(key, value string) {
	if p.Headers == nil {
		p.Headers = make(map[string]string)
	}
	p.Headers[key] = value
}

type PublicMockResponseWithSetHeader struct {
	Headers map[string]string
	Storage map[string]string
}

func (p *PublicMockResponseWithSetHeader) SetHeader(key, value string) {
	if p.Storage == nil {
		p.Storage = make(map[string]string)
	}
	p.Storage[key] = value
}

func TestWithPublicHeaders(t *testing.T) {
	secureHeaders := secure.NewSecureCustom(
		secure.NewContentSecurityPolicy().DefaultSrc("'self'").ImgSrc("'public'"),
		nil,
		nil,
		nil,
		secure.NewServer().Set("PublicServer"),
		[]*secure.CustomHeader{secure.NewCustomHeader("X-Test-Key", "TestVal")},
		nil,
		nil,
	)
	response := &PublicMockResponse{Headers: map[string]string{}}
	secureHeaders.SetHeaders(response)
	if _, ok := response.Headers["Content-Security-Policy"]; !ok {
		t.Errorf("Expected Content-Security-Policy header present")
	}
	if got := response.Headers["Content-Security-Policy"]; got != "default-src 'self'; img-src 'public'" {
		t.Errorf("Expected value for CSP, got %q", got)
	}
	if got := response.Headers["Server"]; got != "PublicServer" {
		t.Errorf("Expected Server header 'PublicServer', got %q", got)
	}
	if got := response.Headers["X-Test-Key"]; got != "TestVal" {
		t.Errorf("Expected X-Test-Key 'TestVal', got %q", got)
	}
	if _, ok := response.Headers["Strict-Transport-Security"]; ok {
		t.Errorf("Did not expect Strict-Transport-Security")
	}
}

func TestFromPresetBasicPublic(t *testing.T) {
	secureHeaders := secure.SecureFromPreset(secure.PresetBasic)
	response := &PublicMockResponse{Headers: map[string]string{}}
	secureHeaders.SetHeaders(response)
	if _, ok := response.Headers["Cache-Control"]; !ok {
		t.Errorf("Expected Cache-Control present")
	}
	if got := response.Headers["Cache-Control"]; got != "no-store" {
		t.Errorf("Expected Cache-Control 'no-store', got %q", got)
	}
	if got := response.Headers["Referrer-Policy"]; got != "strict-origin-when-cross-origin" {
		t.Errorf("Expected Referrer-Policy, got %q", got)
	}
	if got := response.Headers["Server"]; got != "" {
		t.Errorf("Expected Server '', got %q", got)
	}
	if got := response.Headers["Strict-Transport-Security"]; got != "max-age=31536000" {
		t.Errorf("Expected Strict-Transport-Security, got %q", got)
	}
	if got := response.Headers["X-Content-Type-Options"]; got != "nosniff" {
		t.Errorf("Expected X-Content-Type-Options, got %q", got)
	}
	if got := response.Headers["X-Frame-Options"]; got != "SAMEORIGIN" {
		t.Errorf("Expected X-Frame-Options, got %q", got)
	}
	if _, ok := response.Headers["Content-Security-Policy"]; ok {
		t.Errorf("Did not expect Content-Security-Policy to be present")
	}
	if _, ok := response.Headers["Permissions-Policy"]; ok {
		t.Errorf("Did not expect Permissions-Policy to be present")
	}
	if _, ok := response.Headers["Cross-Origin-Opener-Policy"]; ok {
		t.Errorf("Did not expect Cross-Origin-Opener-Policy to be present")
	}
}

func TestFromPresetStrictPublic(t *testing.T) {
	secureHeaders := secure.SecureFromPreset(secure.PresetStrict)
	response := &PublicMockResponse{Headers: map[string]string{}}
	secureHeaders.SetHeaders(response)

	if _, ok := response.Headers["Cache-Control"]; !ok {
		t.Errorf("Expected Cache-Control present")
	}
	if got := response.Headers["Cache-Control"]; got != "no-store" {
		t.Errorf("Expected Cache-Control 'no-store', got %q", got)
	}
	if got := response.Headers["Content-Security-Policy"]; got != "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'" {
		t.Errorf("Expected Content-Security-Policy, got %q", got)
	}
	if got := response.Headers["Cross-Origin-Embedder-Policy"]; got != "require-corp" {
		t.Errorf("Expected Cross-Origin-Embedder-Policy, got %q", got)
	}
	if got := response.Headers["Cross-Origin-Opener-Policy"]; got != "same-origin" {
		t.Errorf("Expected Cross-Origin-Opener-Policy, got %q", got)
	}
	if got := response.Headers["Permissions-Policy"]; got != "geolocation=(), microphone=(), camera=()" {
		t.Errorf("Expected Permissions-Policy, got %q", got)
	}
	if got := response.Headers["Referrer-Policy"]; got != "no-referrer" {
		t.Errorf("Expected Referrer-Policy, got %q", got)
	}
	if got := response.Headers["Server"]; got != "" {
		t.Errorf("Expected Server '', got %q", got)
	}
	if got := response.Headers["Strict-Transport-Security"]; got != "max-age=63072000; includeSubDomains; preload" {
		t.Errorf("Expected Strict-Transport-Security, got %q", got)
	}
	if got := response.Headers["X-Content-Type-Options"]; got != "nosniff" {
		t.Errorf("Expected X-Content-Type-Options, got %q", got)
	}
	if got := response.Headers["X-Frame-Options"]; got != "DENY" {
		t.Errorf("Expected X-Frame-Options, got %q", got)
	}
}

func TestCustomHeadersPublic(t *testing.T) {
	customServer := secure.NewServer().Set("AnotherServer")
	customCSP := secure.NewContentSecurityPolicy().DefaultSrc("'public'").StyleSrc("'test'")
	secureHeaders := secure.NewSecureCustom(
		customCSP,
		nil,
		nil,
		nil,
		customServer,
		nil,
		nil,
		nil,
	)
	response := &PublicMockResponse{Headers: map[string]string{}}
	secureHeaders.SetHeaders(response)
	if got := response.Headers["Server"]; got != "AnotherServer" {
		t.Errorf("Expected Server 'AnotherServer', got %q", got)
	}
	if got := response.Headers["Content-Security-Policy"]; got != "default-src 'public'; style-src 'test'" {
		t.Errorf("Expected Content-Security-Policy, got %q", got)
	}
}