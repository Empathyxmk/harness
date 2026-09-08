package original

import (
	"testing"
)

func TestAbsoluteTruthAndMeaning(t *testing.T) {
	// Just a dummy truth test.
	if true != true {
		t.Error("Absolute truth does not hold")
	}
}