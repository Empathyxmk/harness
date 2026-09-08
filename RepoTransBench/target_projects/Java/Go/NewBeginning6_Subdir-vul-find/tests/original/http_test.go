package original

import (
	"testing"
	"newbeginning6subdir/org/example"
	"strings"
)

func TestHttpApi(t *testing.T) {
	// Basic method call coverage, as actual network not tested
	res, err := example.HttpToUrl("http://example.com")
	if err != nil {
		t.Errorf("HttpToUrl error: %v", err)
	}
	if !strings.Contains(res, "example") {
		t.Errorf("HttpToUrl does not contain example, got: %v", res)
	}

	if example.HttpMethodType("GET") != "GET" {
		t.Errorf("HttpMethodType did not return GET")
	}

	if example.HttpAgent() == "" {
		t.Errorf("HttpAgent returned empty")
	}

	if example.HttpToStringOrNull(nil) != "" {
		t.Errorf("HttpToStringOrNull(nil) did not return empty string")
	}
	if example.HttpToStringOrNull(nil) != "" {
		t.Errorf("HttpToStringOrNull(nil) did not return empty string (repeat)")
	}
}