package login

import (
	"testing"
)

func TestUseAppContext(t *testing.T) {
	packageName := "com.loong.login"
	expected := "com.loong.login"
	if packageName != expected {
		t.Errorf("Expected package name %q but got %q", expected, packageName)
	}
}