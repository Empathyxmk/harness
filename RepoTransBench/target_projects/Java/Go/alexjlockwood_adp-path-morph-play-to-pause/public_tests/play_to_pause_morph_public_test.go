package public_tests

import (
	"testing"

	"pathmorph"
)

func TestInitialStateIsPausePublic(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(false)
	if morph.IsPlaying() {
		t.Errorf("Expected IsPlaying false for initial state false")
	}
	if state := morph.GetState(); state != "PAUSE" {
		t.Errorf("Expected state PAUSE, got %s", state)
	}
}

func TestInitialStateIsPlayingPublic(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(true)
	if !morph.IsPlaying() {
		t.Errorf("Expected IsPlaying true for initial state true")
	}
	if state := morph.GetState(); state != "PLAY" {
		t.Errorf("Expected state PLAY, got %s", state)
	}
}

func TestDoubleToggleFunctionalityPublic(t *testing.T) {
	morph := pathmorph.NewPlayToPauseMorph(false)
	morph.Toggle()
	if !morph.IsPlaying() {
		t.Errorf("After first toggle, expected IsPlaying true, got false")
	}
	if state := morph.GetState(); state != "PLAY" {
		t.Errorf("After first toggle, expected state PLAY, got %s", state)
	}
	morph.Toggle()
	if morph.IsPlaying() {
		t.Errorf("After second toggle, expected IsPlaying false, got true")
	}
	if state := morph.GetState(); state != "PAUSE" {
		t.Errorf("After second toggle, expected state PAUSE, got %s", state)
	}
}