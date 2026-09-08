package public_tests

import (
	"testing"

	"betterprompt"
)

func TestPublicAllExports(t *testing.T) {
	exports := betterprompt.All()
	for _, name := range exports {
		if !betterprompt.HasExport(name) {
			t.Errorf("betterprompt missing export (public): %v", name)
		}
	}
}