package public_tests

import (
	"testing"

	"antiboredom_audiogrep/audiogrep"
)

func TestImportsPublic(t *testing.T) {
	// Just checks import works
	if audiogrep.GetModuleDoc() == "" && audiogrep.GetModuleFile() == "" {
		t.Error("audiogrep package does not provide __file__ or __doc__ equivalent")
	}
}