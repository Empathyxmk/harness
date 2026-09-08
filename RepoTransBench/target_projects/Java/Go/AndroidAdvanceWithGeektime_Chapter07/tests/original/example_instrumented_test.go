package original

import (
	"testing"
)

// This is a minimal non-Android port of the Android instrumentation test.
// In Go, we can't access Android context so we port the test logic as a normal check.

func TestUseAppContext(t *testing.T) {
	// In Android: Assert context packageName == "matrix.tencent.com.matrix_android"
	// Port to Go: Simulate getting a package name from a "context".
	appPackageName := getAppPackageNameSimulated()
	expected := "matrix.tencent.com.matrix_android"
	if appPackageName != expected {
		t.Errorf("Expected package name %s, got %s", expected, appPackageName)
	}
}

// Simulate what the InstrumentationRegistry.getTargetContext().getPackageName() would return.
func getAppPackageNameSimulated() string {
	return "matrix.tencent.com.matrix_android"
}