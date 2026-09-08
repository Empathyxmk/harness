package handlers

import (
	"strings"
	"testing"
)

func TestPlaceholderGcpHandler(t *testing.T) {
	// Should always pass
	if !true {
		t.Errorf("expected true")
	}
}

func TestPlaceholderGcpHandlerDifferent(t *testing.T) {
	if !strings.Contains("fastapi_events_gcp_handler", "gcp") {
		t.Errorf(`expected "fastapi_events_gcp_handler" to contain "gcp"`)
	}
}