package share

import (
	"testing"
)

func TestUseAppContext(t *testing.T) {
	packageName := "com.loong.share"
	expected := "com.loong.share"
	if packageName != expected {
		t.Errorf("Expected package name %q but got %q", expected, packageName)
	}
}