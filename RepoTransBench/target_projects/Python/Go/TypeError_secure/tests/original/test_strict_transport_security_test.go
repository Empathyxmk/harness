package original

import (
	"TypeError_secure/secure"
	"testing"
	"strings"
)

func TestDefaultHeaderValue(t *testing.T) {
	sts := secure.NewStrictTransportSecurity()
	if !strings.Contains(sts.HeaderValue(), "max-age") {
		t.Errorf("Expected 'max-age' in header value, got %q", sts.HeaderValue())
	}
}

func TestSetAndClearDirectives(t *testing.T) {
	sts := secure.NewStrictTransportSecurity()
	sts.MaxAge(1234)
	if !strings.Contains(sts.HeaderValue(), "max-age=1234") {
		t.Errorf("Expected 'max-age=1234' in header value, got %q", sts.HeaderValue())
	}
	sts.IncludeSubdomains()
	if !strings.Contains(sts.HeaderValue(), "includeSubDomains") {
		t.Errorf("Expected 'includeSubDomains' in header value, got %q", sts.HeaderValue())
	}
	sts.Preload()
	if !strings.Contains(sts.HeaderValue(), "preload") {
		t.Errorf("Expected 'preload' in header value, got %q", sts.HeaderValue())
	}
	val := sts.HeaderValue()
	if !(strings.Contains(val, "max-age=1234") && strings.Contains(val, "includeSubDomains") && strings.Contains(val, "preload")) {
		t.Errorf("Expected all directives in header value, got %q", val)
	}
	sts.Clear()
	if sts.HeaderValue() != "max-age=31536000" {
		t.Errorf("Expected default header value after clear, got %q", sts.HeaderValue())
	}
}

func TestSetCustomValue(t *testing.T) {
	sts := secure.NewStrictTransportSecurity()
	sts.MaxAge(1).IncludeSubdomains()
	sts.Set("something-custom")
	if sts.HeaderValue() != "something-custom" {
		t.Errorf("Expected custom header value, got %q", sts.HeaderValue())
	}
}

func TestNoDuplicateDirectives(t *testing.T) {
	sts := secure.NewStrictTransportSecurity()
	sts.IncludeSubdomains().IncludeSubdomains()
	count := strings.Count(sts.HeaderValue(), "includeSubDomains")
	if count != 1 {
		t.Errorf("Expected includeSubDomains only once, got %d", count)
	}
}