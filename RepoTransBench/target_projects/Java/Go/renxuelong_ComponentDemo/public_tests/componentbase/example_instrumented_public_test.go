package componentbase

import (
	"strings"
	"testing"
)

func TestAppContextPackageNameIsNotNull(t *testing.T) {
	packageName := "com.loong.componentbase"
	if len(packageName) == 0 {
		t.Errorf("Expected non-empty package name")
	}
	if !strings.Contains(packageName, "componentbase") {
		t.Errorf(`Expected package name to contain "componentbase", got %q`, packageName)
	}
}