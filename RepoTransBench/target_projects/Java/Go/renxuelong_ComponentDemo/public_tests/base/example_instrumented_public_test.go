package base

import (
	"strings"
	"testing"
)

func TestPackageNameContainsBase(t *testing.T) {
	packageName := "com.loong.base"
	if !strings.Contains(packageName, "base") {
		t.Errorf(`Expected package name to contain "base", got %q`, packageName)
	}
}