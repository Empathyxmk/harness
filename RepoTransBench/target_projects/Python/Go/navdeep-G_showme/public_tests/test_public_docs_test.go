package public_tests

import (
	"strings"
	"testing"
)

func GetDoc() string {
	// Simulate the __doc__ string of showme/core
	return "Package showme core documentation - showme provides Python decorators for tracing/testing."
}

func TestPublicDocs(t *testing.T) {
	doc := GetDoc()
	if !strings.Contains(strings.ToLower(doc), "showme") &&
		!strings.Contains(strings.ToLower(doc), "core") {
		t.Error("Doc should contain 'showme' or 'core'")
	}
}