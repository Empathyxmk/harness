package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestXFrameOptionsDefaults(t *testing.T) {
	xfo := secure.NewXFrameOptions()
	if xfo.HeaderValue() != "SAMEORIGIN" {
		t.Errorf("Expected default X-Frame-Options value 'SAMEORIGIN', got %q", xfo.HeaderValue())
	}
}

func TestSetAndClearValue(t *testing.T) {
	xfo := secure.NewXFrameOptions()
	xfo.Set("foo")
	if xfo.HeaderValue() != "foo" {
		t.Errorf("Expected header_value to be 'foo', got %q", xfo.HeaderValue())
	}
	xfo.Clear()
	if xfo.HeaderValue() != "SAMEORIGIN" {
		t.Errorf("Expected header_value after clear to be 'SAMEORIGIN', got %q", xfo.HeaderValue())
	}
}

func TestDenyAndSameoriginMethods(t *testing.T) {
	xfo := secure.NewXFrameOptions()
	xfo.Deny()
	if xfo.HeaderValue() != "DENY" {
		t.Errorf("Expected header_value to be 'DENY', got %q", xfo.HeaderValue())
	}
	xfo.Sameorigin()
	if xfo.HeaderValue() != "SAMEORIGIN" {
		t.Errorf("Expected header_value to be 'SAMEORIGIN', got %q", xfo.HeaderValue())
	}
}