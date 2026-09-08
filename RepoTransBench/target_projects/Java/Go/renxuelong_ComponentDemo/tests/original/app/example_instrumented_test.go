package app

import (
	"testing"
)

func TestUseAppContext(t *testing.T) {
	packageName := "com.loong.componentdemo"
	expected := "com.loong.componentdemo"
	if packageName != expected {
		t.Errorf("Expected package name %q but got %q", expected, packageName)
	}
}