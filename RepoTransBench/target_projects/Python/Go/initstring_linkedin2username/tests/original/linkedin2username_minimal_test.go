package original

import (
	"testing"

	"github.com/example/initstring_linkedin2username"
)

func TestImportLinkedin2username(t *testing.T) {
	mut := linkedin2username.NewNameMutator("Test User")
	if mut == nil {
		t.Fatalf("expected non-nil NameMutator")
	}
}

// Note: the Python test uses monkeypatch and sys module name magic to simulate __main__.
// In Go, we simulate main() invocation explicitly.
func TestMainInvocation(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("Panic on main invocation: %v", r)
		}
	}()
	// Call the main function, expected not to panic.
	// If main() requires arguments/env, those should be set up accordingly for the tests.
	linkedin2username.Main()
}