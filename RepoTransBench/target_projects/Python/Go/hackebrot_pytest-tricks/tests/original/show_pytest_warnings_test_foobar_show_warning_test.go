package original

import (
	"testing"
)

func TestWarns(t *testing.T) {
	// There's no direct equivalent of pytest.warns in Go.
	// We use t.Log and the testing package does not capture warnings.
	// Instead, we'll show that a warning message can be emitted.
	t.Log("this is a warning")
}