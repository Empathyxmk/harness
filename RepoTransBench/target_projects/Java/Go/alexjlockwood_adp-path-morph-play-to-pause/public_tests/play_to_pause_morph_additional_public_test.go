package public_tests

import (
	"testing"

	"pathmorph"
)

func TestMultipleTogglesPublic(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(true)
	expected := true
	for i := 0; i < 4; i++ {
		morph.Toggle()
		expected = !expected
		if morph.IsPlaying() != expected {
			t.Errorf("Toggle #%d: want playing=%v, got %v", i+1, expected, morph.IsPlaying())
		}
	}
}

func TestGetStateStringsPublic(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(false)
	if got := morph.GetState(); got != "PAUSE" {
		t.Errorf("Initial GetState: want PAUSE, got %s", got)
	}
	morph.Toggle()
	if got := morph.GetState(); got != "PLAY" {
		t.Errorf("After toggle GetState: want PLAY, got %s", got)
	}
}

func TestEdgeCaseNoTogglePublic(t *testing.T) {
	morphPause := pathmorph.NewPlayToPauseMorph(false)
	if got := morphPause.GetState(); got != "PAUSE" {
		t.Errorf("morphPause: want PAUSE, got %s", got)
	}
	morphPlay := pathmorph.NewPlayToPauseMorph(true)
	if got := morphPlay.GetState(); got != "PLAY" {
		t.Errorf("morphPlay: want PLAY, got %s", got)
	}
}