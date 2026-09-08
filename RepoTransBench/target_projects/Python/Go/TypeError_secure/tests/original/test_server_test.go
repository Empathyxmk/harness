package original

import (
	"TypeError_secure/secure"
	"testing"
)

func TestDefaultServer(t *testing.T) {
	serverHeader := secure.NewServer()
	if serverHeader.HeaderValue() != "" {
		t.Errorf("Expected default Server header value '', got %q", serverHeader.HeaderValue())
	}
}

func TestSetCustomServer(t *testing.T) {
	serverHeader := secure.NewServer().Set("CustomServer")
	if serverHeader.HeaderValue() != "CustomServer" {
		t.Errorf("Expected Server header value 'CustomServer', got %q", serverHeader.HeaderValue())
	}
}

func TestClearServer(t *testing.T) {
	serverHeader := secure.NewServer().Set("CustomServer").Clear()
	if serverHeader.HeaderValue() != "" {
		t.Errorf("Expected cleared Server header value '', got %q", serverHeader.HeaderValue())
	}
}