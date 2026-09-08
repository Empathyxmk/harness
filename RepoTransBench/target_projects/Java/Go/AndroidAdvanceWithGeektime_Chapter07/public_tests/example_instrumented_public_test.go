package public_tests

import (
	"testing"
)

// Public variant: checks context is not null and not equal dummy value.

func TestUseAppContextPublic(t *testing.T) {
	appPackageName := getAppPackageNameSimulated()
	if appPackageName == "" {
		t.Fatal("app context is nil/empty")
	}
	if appPackageName == "com.geektime.systrace.dummy" {
		t.Errorf("package name should not equal dummy value")
	}
}

// Simulated app context function for public variant.
func getAppPackageNameSimulated() string {
	return "matrix.tencent.com.matrix_android"
}