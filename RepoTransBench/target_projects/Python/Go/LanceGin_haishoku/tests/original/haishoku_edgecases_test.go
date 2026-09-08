package original

import (
	"testing"
	"lancegin_haishoku/haishoku"
)

func TestHaishokuInstanceReturnType(t *testing.T) {
	obj := haishoku.LoadHaishoku("demo/demo_01.png")
	if obj != haishoku.HaishokuClassValue() {
		t.Fatalf("LoadHaishoku returned %v, want Haishoku class", obj)
	}
}
// ... other valid existing tests ...