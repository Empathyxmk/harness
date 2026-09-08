package public_tests

import (
	"strings"
	"testing"
)

func TestUseAppContextDifferentPackage(t *testing.T) {
	appContextPackageName := "top.niunaijun.blackobfuscator.asplugin"
	if !strings.HasPrefix(appContextPackageName, "top.") {
		t.Errorf("expected package name to start with 'top.', got %q", appContextPackageName)
	}
}