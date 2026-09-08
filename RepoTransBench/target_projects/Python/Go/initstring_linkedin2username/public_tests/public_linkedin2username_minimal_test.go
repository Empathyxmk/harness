package public_tests

import (
	"testing"
	"github.com/example/initstring_linkedin2username"
)

func TestPublicImportLinkedin2Username(t *testing.T) {
	nm := linkedin2username.NewNameMutator("Lena Horne")
	if nm == nil {
		t.Fatalf("Expected non-nil NameMutator")
	}
}

func TestPublicMainInvocation(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("Panic during main invocation: %v", r)
		}
	}()
	linkedin2username.Main()
}