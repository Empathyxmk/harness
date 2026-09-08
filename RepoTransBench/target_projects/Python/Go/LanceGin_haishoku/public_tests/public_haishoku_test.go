package public_tests

import (
	"testing"
	"lancegin_haishoku/haishoku"
)

func TestHaishokuGetPalettePublic(t *testing.T) {
	hs := haishoku.NewHaishokuWithImage("demo/demo_01.png")
	palette := hs.Palette
	if len(palette) != 6 {
		t.Fatalf("expected palette length 6, got %d", len(palette))
	}
	for i, color := range palette {
		if len(color) != 3 {
			t.Fatalf("palette[%d] has len=%d, want 3", i, len(color))
		}
	}
}