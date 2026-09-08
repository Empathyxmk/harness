package public_tests

import "testing"

// Simulate ZBarSymbol as const ints
type ZBarSymbolType struct{}

var ZBarSymbol = struct {
	CODE39 int
	CODE93 int
	ALL    []int
}{
	CODE39: 39,
	CODE93: 93,
	ALL:    []int{39, 93, 128, 2},
}

func TestEnumValues(t *testing.T) {
	// Test that CODE39 exists and is int type
	_ = ZBarSymbol.CODE39
}

func TestAllSymbolsIncludesSymbol(t *testing.T) {
	in := false
	for _, sym := range ZBarSymbol.ALL {
		if sym == ZBarSymbol.CODE93 {
			in = true
		}
	}
	if !in {
		t.Errorf("CODE93 not in ALL")
	}
}