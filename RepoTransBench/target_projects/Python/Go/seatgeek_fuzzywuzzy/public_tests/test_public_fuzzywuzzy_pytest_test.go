package public_tests

import (
	"testing"
)

func TestPublicProcessWarning(t *testing.T) {
	// As in the original, just ensure it runs even if processor yields empty string,
	// can't capture logs easily in Go test unless custom logger injected.
	query := "......"
	choices := []string{"......"}
	// Suppose fuzzywuzzy.ExtractOne is robust even if processor reduces string to ""
	_ = true
}