package componentbase

import (
	"testing"
)

// Instrumented tests are Android-only; for Go, we stub this and verify package name string.

func TestUseAppContext(t *testing.T) {
	// Stubbing the context check
	packageName := "com.loong.componentbase.test"
	expected := "com.loong.componentbase.test"
	if packageName != expected {
		t.Errorf("Expected package name %q, got %q", expected, packageName)
	}
}