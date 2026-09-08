package tests

import (
	"testing"
	"bumpversion"
)

func TestModuleHasExpectedMinimalExports(t *testing.T) {
	attrs := bumpversion.Attrs()
	hasDescription := false
	for _, attr := range attrs {
		if attr == "DESCRIPTION" {
			hasDescription = true
			break
		}
	}
	if !hasDescription {
		t.Errorf("Expected DESCRIPTION in bumpversion attributes")
	}
}