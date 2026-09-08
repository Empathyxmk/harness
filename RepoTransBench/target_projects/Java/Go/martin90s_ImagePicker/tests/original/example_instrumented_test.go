package original

import (
	"testing"
)

// Simulate "Context" with just a package name
type AppContext struct {
	PackageName string
}

func TestExampleInstrumented_UseAppContext(t *testing.T) {
	appContext := AppContext{PackageName: "com.imnjh.imagepicker"}
	if appContext.PackageName != "com.imnjh.imagepicker" {
		t.Errorf("Expected package name com.imnjh.imagepicker, got %s", appContext.PackageName)
	}
}