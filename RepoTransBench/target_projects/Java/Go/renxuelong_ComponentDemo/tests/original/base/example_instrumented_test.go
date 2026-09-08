package base

import (
	"testing"
)

func TestUseAppContext(t *testing.T) {
	packageName := "com.loong.base.test"
	expected := "com.loong.base.test"
	if packageName != expected {
		t.Errorf("Expected package name %q but got %q", expected, packageName)
	}
}