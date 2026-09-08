package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestCustomHeaderInitAndProperties(t *testing.T) {
	ch := secure.NewCustomHeader("X-Sample-Header", "init-value")
	if ch.HeaderName() != "X-Sample-Header" {
		t.Errorf("Expected header_name 'X-Sample-Header', got %q", ch.HeaderName())
	}
	if ch.HeaderValue() != "init-value" {
		t.Errorf("Expected header_value 'init-value', got %q", ch.HeaderValue())
	}
}

func TestCustomHeaderSetChainAndOverride(t *testing.T) {
	ch := secure.NewCustomHeader("X-Chain", "val1")
	ret := ch.Set("val2")
	if ch.HeaderValue() != "val2" {
		t.Errorf("Expected header_value to be 'val2', got %q", ch.HeaderValue())
	}
	if ret != ch {
		t.Errorf("Expected Set() to return same CustomHeader instance")
	}
}

func TestCustomHeaderSetEdgeCases(t *testing.T) {
	ch := secure.NewCustomHeader("X-Edge", "start")
	ch.Set("")
	if ch.HeaderValue() != "" {
		t.Errorf("Expected header_value to be empty string, got %q", ch.HeaderValue())
	}
	ch.Set("123")
	if ch.HeaderValue() != "123" {
		t.Errorf("Expected header_value to be '123', got %q", ch.HeaderValue())
	}
}