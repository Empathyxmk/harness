package original

import (
	"testing"

	"clippingbasic/tests"
)

func TestPreconditions(t *testing.T) {
	activity := tests.NewMainActivity()
	fragment := activity.GetFragment()
	if activity == nil {
		t.Errorf("Test activity is nil")
	}
	if fragment == nil {
		t.Errorf("Test fragment is nil")
	}
	if activity.FindViewByID("frame") == nil {
		t.Errorf("Clipped frame view is nil")
	}
	if activity.FindViewByID("textView") == nil {
		t.Errorf("Text view is nil")
	}
}

func TestClipping(t *testing.T) {
	activity := tests.NewMainActivity()
	clippedView := activity.FindViewByID("frame")
	if clippedView.GetClipToOutline() {
		t.Errorf("Initially, should not be clipped")
	}
	// Simulate button click
	tests.SimulateButtonClick(activity)
	if !clippedView.GetClipToOutline() {
		t.Errorf("View was not clipped after button click")
	}
}