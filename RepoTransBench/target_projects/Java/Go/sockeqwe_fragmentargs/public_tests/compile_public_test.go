package public_tests

import (
	"testing"
)

type ColorPublic int

const (
	RED ColorPublic = iota
	GREEN
	BLUE
)

func ColorPublicValueOf(name string) ColorPublic {
	switch name {
	case "RED":
		return RED
	case "GREEN":
		return GREEN
	case "BLUE":
		return BLUE
	default:
		panic("unknown")
	}
}

func TestSimpleCompileTestPublicVariant(t *testing.T) {
	if got := ColorPublicValueOf("GREEN"); got != GREEN {
		t.Errorf("Expected GREEN, got %v", got)
	}
}