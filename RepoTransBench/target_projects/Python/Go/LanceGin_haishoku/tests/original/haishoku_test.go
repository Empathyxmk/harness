package original

import (
	"testing"
	"lancegin_haishoku/haishoku"
)

func TestHaishokuInstance(t *testing.T) {
	obj := haishoku.LoadHaishoku("demo/demo_01.png")
	// The bug: loadHaishoku returns the class, not an instance.
	if obj != haishoku.HaishokuClassValue() {
		t.Fatalf("LoadHaishoku returned %v, want Haishoku class", obj)
	}
}
// ... other valid existing tests ...