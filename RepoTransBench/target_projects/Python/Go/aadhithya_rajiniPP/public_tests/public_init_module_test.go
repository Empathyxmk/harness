package public_tests

import (
	"strings"
	"testing"

	"yourmodule/rajinipp"
	"yourmodule/rajinipp/runner"
)

func TestPublicVersionAndStr(t *testing.T) {
	if rajinipp.Version == "" {
		t.Error("rajinipp.Version should exist and not be empty")
	}
	if rajinipp.VersionStr == "" {
		t.Error("rajinipp.VersionStr should exist and not be empty")
	}
	if !strings.HasPrefix(rajinipp.VersionStr, "rajini") {
		t.Errorf("VersionStr should start with 'rajini', got: %q", rajinipp.VersionStr)
	}
	if len(rajinipp.All) == 0 {
		t.Error("rajinipp.All should exist and not be empty")
	}
}

func TestPublicRppRunnerImported(t *testing.T) {
	if typ := runner.TypeName(rajinipp.Rpp); typ != "RppRunner" {
		t.Errorf("Expected type RppRunner, got %s", typ)
	}
}