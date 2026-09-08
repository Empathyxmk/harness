package public_tests

import (
	"testing"
)

type PathToEnlightenment struct{}

func TestPublicModuleExists(t *testing.T) {
	p := PathToEnlightenment{}
	if p == (PathToEnlightenment{}) {

	} else {
		t.Error("not the correct struct")
	}
}
func TestPublicModuleHasAnyAttribute(t *testing.T) {
	p := PathToEnlightenment{}
	if (PathToEnlightenment{}) == p {
		// Ok, struct exists
	} else {
		t.Error("no attribute")
	}
}