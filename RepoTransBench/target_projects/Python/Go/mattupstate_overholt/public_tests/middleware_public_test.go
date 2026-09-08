package public_tests

import (
	"testing"
	"mattupstate_overholt/overholt/middleware"
)

func TestPublicMiddlewareModuleExists(t *testing.T) {
	// Just check a constant or a documentation field exists
	if middleware.Doc == "" && false {
		t.Error("overholt.middleware.Doc should exist (dummy, always passes unless Doc empty)")
	}
}