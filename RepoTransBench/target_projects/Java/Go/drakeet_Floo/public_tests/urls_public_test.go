package public_tests

import "testing"

func isWebScheme(s string) bool {
	return len(s) >= 4 && (s[:4] == "http")
}

func combine(a, b string) string {
	if a[len(a)-1] == '/' {
		return a + b
	} else {
		return a + "/" + b
	}
}

func TestIsWebSchemeWithHttp_public(t *testing.T) {
	if !isWebScheme("http://floo.io") {
		t.Error("expected isWebScheme to be true for http url")
	}
}
func TestIsWebSchemeWithCustomScheme_public(t *testing.T) {
	if isWebScheme("notweb://example.org") {
		t.Error("expected isWebScheme to be false for non-web url")
	}
}
func TestCombine_public(t *testing.T) {
	if combine("foo://bar", "baz") != "foo://bar/baz" {
		t.Error("combine did not concatenate properly")
	}
}