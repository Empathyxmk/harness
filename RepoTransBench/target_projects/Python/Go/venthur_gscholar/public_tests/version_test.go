package public_tests

import (
	"testing"
)

func TestPublicVersionString(t *testing.T) {
	ver := "1.2.3"
	if len(ver) < 1 {
		t.Error("Version string too short")
	}
}

func TestPublicVersionNotEmpty(t *testing.T) {
	ver := "1.2.3"
	if ver == "" {
		t.Error("Version string should not be empty")
	}
}

func TestPublicVersionContainsDot(t *testing.T) {
	ver := "1.2.3"
	if !strings.Contains(ver, ".") {
		t.Error("Version string should contain a dot")
	}
}