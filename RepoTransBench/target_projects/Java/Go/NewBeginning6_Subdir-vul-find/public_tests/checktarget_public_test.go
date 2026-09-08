package public_tests

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestIsValidUrlPublic(t *testing.T) {
	if !example.CheckTargetIsTarget("https://www.wikipedia.org") {
		t.Errorf("Should be valid: https://www.wikipedia.org")
	}
	if !example.CheckTargetIsTarget("http://localhost:8000/test") {
		t.Errorf("Should be valid: http://localhost:8000/test")
	}
	if example.CheckTargetIsTarget("file:///tmp/test.txt") {
		t.Errorf("Should not be valid: file:///tmp/test.txt")
	}
	if example.CheckTargetIsTarget("not_a_url") {
		t.Errorf("Should not be valid: not_a_url")
	}
}

func TestHostLogicPublic(t *testing.T) {
	if example.CheckTargetHost("http://example.com/page") != "example.com" {
		t.Errorf("Host for example.com/page wrong")
	}
	if example.CheckTargetHost("https://localhost:1234") != "localhost" {
		t.Errorf("Host for localhost:1234 wrong")
	}
	if example.CheckTargetHost("file:///tmp/test.txt") != "" {
		t.Errorf("Host for file url should be empty")
	}
}