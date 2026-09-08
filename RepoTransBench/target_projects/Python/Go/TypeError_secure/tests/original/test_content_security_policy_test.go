package original

import (
	"TypeError_secure/secure"
	"testing"
	"strings"
)

func TestDefaultCSP(t *testing.T) {
	csp := secure.NewContentSecurityPolicy()
	expected := "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'"
	if csp.HeaderValue() != expected {
		t.Errorf("Expected default CSP: %q, got %q", expected, csp.HeaderValue())
	}
}

func TestCustomPolicy(t *testing.T) {
	csp := secure.NewContentSecurityPolicy().
		DefaultSrc("'self'").
		ImgSrc("'self'", "cdn.example.com")
	expected := "default-src 'self'; img-src 'self' cdn.example.com"
	if csp.HeaderValue() != expected {
		t.Errorf("Expected custom policy value: %q, got %q", expected, csp.HeaderValue())
	}
}

func TestAddScriptSrc(t *testing.T) {
	csp := secure.NewContentSecurityPolicy().ScriptSrc("'self'", "'unsafe-inline'")
	if !strings.Contains(csp.HeaderValue(), "script-src 'self' 'unsafe-inline'") {
		t.Errorf("Expected script-src directive, got %q", csp.HeaderValue())
	}
}

func TestClearPolicy(t *testing.T) {
	csp := secure.NewContentSecurityPolicy().DefaultSrc("'self'").Clear()
	expected := "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'"
	if csp.HeaderValue() != expected {
		t.Errorf("Expected default after clear, got %q", csp.HeaderValue())
	}
}