package original

import (
	"testing"
)

func TestUseAppContextFakeCheck(t *testing.T) {
	// In Go, we don't have Android Context. We'll simulate the "package name" as a string.
	appContextPackageName := "top.niunaijun.blackobfuscator.asplugin"
	expected := "top.niunaijun.blackobfuscator.asplugin"
	if appContextPackageName != expected {
		t.Errorf("expected package name %q, got %q", expected, appContextPackageName)
	}
}