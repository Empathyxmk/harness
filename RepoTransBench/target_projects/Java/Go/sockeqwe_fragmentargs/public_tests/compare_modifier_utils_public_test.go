package public_tests

import (
	"testing"
)

func TestCompareModifiersPublicVariant(t *testing.T) {
	const Public = 1 << 0
	const Private = 1 << 1
	const Static = 1 << 2

	combined := Public | Static
	if combined&Public == 0 {
		t.Error("Expected combined to contain Public")
	}
	if combined&Static == 0 {
		t.Error("Expected combined to contain Static")
	}
	if combined&Private != 0 {
		t.Error("Expected combined to not contain Private")
	}
}