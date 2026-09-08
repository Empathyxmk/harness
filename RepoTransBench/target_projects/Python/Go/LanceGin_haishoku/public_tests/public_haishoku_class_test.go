package public_tests

import (
	"testing"
	"lancegin_haishoku/haishoku"
)

func TestHaishokuMainColorDistinct(t *testing.T) {
	hs := haishoku.NewHaishokuWithImage("demo/demo_01.png")
	main := hs.MainColor
	if len(main) != 3 {
		t.Fatalf("main color len=%d, want 3", len(main))
	}
	for _, v := range main {
		if v < 0 || v > 255 {
			t.Errorf("main color value out of range: %v", v)
		}
	}
	if main[0] == 199 && main[1] == 146 && main[2] == 117 {
		t.Errorf("main color should not be (199,146,117)")
	}
}