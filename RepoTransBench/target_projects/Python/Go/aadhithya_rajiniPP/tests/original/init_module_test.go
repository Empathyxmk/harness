package original

import (
	"strings"
	"testing"

	"yourmodule/rajinipp"
	"yourmodule/rajinipp/runner"
)

func TestVersionAndStr(t *testing.T) {
	if rajinipp.Version == "" {
		t.Error("rajinipp.Version should exist and not be empty")
	}
	if rajinipp.VersionStr == "" {
		t.Error("rajinipp.VersionStr should exist and not be empty")
	}
	if !strings.Contains(rajinipp.VersionStr, "rajini++") {
		t.Errorf("rajinipp.VersionStr should contain 'rajini++', got %q", rajinipp.VersionStr)
	}
	if len(rajinipp.All) == 0 {
		t.Error("rajinipp.All should be present and not empty")
	}
}

func TestRppRunnerImported(t *testing.T) {
	if _, ok := interface{}(rajinipp.Rpp).(*runner.RppRunner); !ok {
		t.Fatal("rajinipp.Rpp should be an instance of runner.RppRunner")
	}
}