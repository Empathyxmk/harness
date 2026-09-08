package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestDefaultXContentTypeOptions(t *testing.T) {
	xcto := secure.NewXContentTypeOptions()
	if xcto.HeaderValue() != "nosniff" {
		t.Errorf("Expected default X-Content-Type-Options 'nosniff', got %q", xcto.HeaderValue())
	}
}

func TestSetCustomValue(t *testing.T) {
	xcto := secure.NewXContentTypeOptions().Set("custom-value")
	if xcto.HeaderValue() != "custom-value" {
		t.Errorf("Expected header value 'custom-value', got %q", xcto.HeaderValue())
	}
}

func TestNosniff(t *testing.T) {
	xcto := secure.NewXContentTypeOptions().Nosniff()
	if xcto.HeaderValue() != "nosniff" {
		t.Errorf("Expected 'nosniff' value, got %q", xcto.HeaderValue())
	}
}

func TestClear(t *testing.T) {
	xcto := secure.NewXContentTypeOptions().Set("custom-value").Clear()
	if xcto.HeaderValue() != "nosniff" {
		t.Errorf("Expected clear to reset to 'nosniff', got %q", xcto.HeaderValue())
	}
}