package original

import (
	"testing"

	"pathmorph"
)

func TestMultipleToggles(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(false)
	expected := false
	for i := 0; i < 5; i++ {
		morph.Toggle()
		expected = !expected
		if morph.IsPlaying() != expected {
			t.Errorf("Toggle #%d: want playing=%v, got %v", i+1, expected, morph.IsPlaying())
		}
	}
}

func TestGetStateStrings(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(true)
	if got := morph.GetState(); got != "PLAY" {
		t.Errorf("Initial GetState: want PLAY, got %s", got)
	}
	morph.Toggle()
	if got := morph.GetState(); got != "PAUSE" {
		t.Errorf("After toggle GetState: want PAUSE, got %s", got)
	}
}

func TestEdgeCaseNoToggle(t *testing.T) {
	morphPlay := pathmorph.NewPlayToPauseMorph(true)
	if got := morphPlay.GetState(); got != "PLAY" {
		t.Errorf("morphPlay: want PLAY, got %s", got)
	}
	morphPause := pathmorph.NewPlayToPauseMorph(false)
	if got := morphPause.GetState(); got != "PAUSE" {
		t.Errorf("morphPause: want PAUSE, got %s", got)
	}
}