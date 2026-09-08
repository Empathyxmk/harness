package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestDefaultCOOP(t *testing.T) {
	coop := secure.NewCrossOriginOpenerPolicy()
	if coop.HeaderValue() != "same-origin" {
		t.Errorf("Expected default COOP 'same-origin', got %q", coop.HeaderValue())
	}
}

func TestSetCustomPolicy(t *testing.T) {
	coop := secure.NewCrossOriginOpenerPolicy().Set("custom-policy")
	if coop.HeaderValue() != "custom-policy" {
		t.Errorf("Expected COOP 'custom-policy', got %q", coop.HeaderValue())
	}
}

func TestSameOrigin(t *testing.T) {
	coop := secure.NewCrossOriginOpenerPolicy().SameOrigin()
	if coop.HeaderValue() != "same-origin" {
		t.Errorf("Expected COOP 'same-origin', got %q", coop.HeaderValue())
	}
}

func TestSameOriginAllowPopups(t *testing.T) {
	coop := secure.NewCrossOriginOpenerPolicy().SameOriginAllowPopups()
	if coop.HeaderValue() != "same-origin-allow-popups" {
		t.Errorf("Expected COOP 'same-origin-allow-popups', got %q", coop.HeaderValue())
	}
}

func TestUnsafeNone(t *testing.T) {
	coop := secure.NewCrossOriginOpenerPolicy().UnsafeNone()
	if coop.HeaderValue() != "unsafe-none" {
		t.Errorf("Expected COOP 'unsafe-none', got %q", coop.HeaderValue())
	}
}

func TestClearPolicy(t *testing.T) {
	coop := secure.NewCrossOriginOpenerPolicy().Set("custom-policy").Clear()
	if coop.HeaderValue() != "same-origin" {
		t.Errorf("Expected default COOP after clear, got %q", coop.HeaderValue())
	}
}