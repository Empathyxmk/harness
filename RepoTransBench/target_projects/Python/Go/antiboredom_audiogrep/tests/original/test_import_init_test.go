package original

import (
	"testing"

	"antiboredom_audiogrep/audiogrep"
)

func TestImportFromInit(t *testing.T) {
	// Test that audiogrep package exposes the required names.
	// In Go, we'll check that the functions exist as exported names.
	// We simply invoke them to ensure they are "linkable".
	_ = audiogrep.ConvertToWav
	_ = audiogrep.Transcribe
}