package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestDefaultPermissionsPolicy(t *testing.T) {
	policy := secure.NewPermissionsPolicy()
	if policy.HeaderValue() != "geolocation=(), microphone=(), camera=()" {
		t.Errorf("Expected default Permissions-Policy value, got %q", policy.HeaderValue())
	}
}

func TestCustomPermissionsPolicy(t *testing.T) {
	policy := secure.NewPermissionsPolicy().Camera("'self'").Geolocation("'none'")
	if policy.HeaderValue() != "camera=('self'), geolocation=('none')" {
		t.Errorf("Expected 'camera=('self'), geolocation=('none')', got %q", policy.HeaderValue())
	}
}

func TestClearPermissionsPolicy(t *testing.T) {
	policy := secure.NewPermissionsPolicy().Camera("'self'").Clear()
	if policy.HeaderValue() != "geolocation=(), microphone=(), camera=()" {
		t.Errorf("Expected default Permissions-Policy value after clear, got %q", policy.HeaderValue())
	}
}

func TestAddDirective(t *testing.T) {
	policy := secure.NewPermissionsPolicy().AddDirective("microphone", "'self'")
	if contains := containsStr(policy.HeaderValue(), "microphone=('self')"); !contains {
		t.Errorf("Expected 'microphone=('self')' in header value, got %q", policy.HeaderValue())
	}
}

// Helper for substring check
func containsStr(s, substr string) bool {
	return len(s) >= len(substr) && (s == substr || len(s) > len(substr) && (containsStr(s[1:], substr) || containsStr(s[:len(s)-1], substr)))
}