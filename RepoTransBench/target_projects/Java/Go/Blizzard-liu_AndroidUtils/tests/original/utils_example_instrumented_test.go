package original

import (
    "testing"
)

func TestUtilsUseAppContext(t *testing.T) {
    // Simulate expected package name for utils
    utilsPackageName := "com.example.utils.test"
    if utilsPackageName != "com.example.utils.test" {
        t.Errorf("expected package name %q but got %q", "com.example.utils.test", utilsPackageName)
    }
}