package original

import (
	"testing"

	"betterprompt"
)

func TestAllExports(t *testing.T) {
	exports := betterprompt.All()
	for _, name := range exports {
		if !betterprompt.HasExport(name) {
			t.Errorf("betterprompt missing export: %v", name)
		}
	}
}