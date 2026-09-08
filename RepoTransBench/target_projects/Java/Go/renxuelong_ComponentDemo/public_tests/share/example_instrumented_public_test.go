package share

import (
	"strings"
	"testing"
)

func TestAppContextPackageNameContainsShare(t *testing.T) {
	packageName := "com.loong.share"
	if !strings.Contains(packageName, "share") {
		t.Errorf(`Expected package name to contain "share", got %q`, packageName)
	}
}