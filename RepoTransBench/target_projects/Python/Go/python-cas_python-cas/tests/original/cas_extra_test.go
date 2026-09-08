package original

import (
	"testing"
	"casproject/cas"
)

func TestModuleSmoke(t *testing.T) {
	// Verify public vars exist (in Go, that package cas loads)
	if cas.Version == "" && cas.SomeOtherExport == "" {
		t.Errorf("CAS package missing expected attributes")
	}
}

func TestHasClassesAndFunctions(t *testing.T) {
	if !cas.CASClientExported() &&
		!cas.CASClientV2Exported() &&
		!cas.CASClientV3Exported() &&
		!cas.CasResponseExported() {
		t.Errorf("Expected at least one public API to be exported")
	}
}

func TestLoginURLSignature(t *testing.T) {
	if cas.LoginURLExported() {
		url := cas.LoginURL("http://example.com", "http://service/callback")
		if !strings.Contains(url, "example.com") {
			t.Errorf("Expected 'example.com' part of generated login url, got %s", url)
		}
	}
}