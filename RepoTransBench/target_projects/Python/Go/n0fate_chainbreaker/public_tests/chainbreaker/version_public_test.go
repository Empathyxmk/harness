package chainbreaker

import (
	"strings"
	"testing"
)

func TestPublicVersionAttribute(t *testing.T) {
	v := Version()
	if v == "" {
		t.Error("Expected a version string")
	}
	if !strings.Contains(v, ".") || len(strings.Split(v, ".")) < 2 {
		t.Errorf("Version should be at least major.minor format, got %q", v)
	}
}

func TestPublicVersionModuleDoc(t *testing.T) {
	if Doc() == "" {
		t.Error("Expected Version module to have doc (Doc())")
	}
}