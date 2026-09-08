package public_tests

import (
	"testing"

	"github.com/othersideai/chronology/chronological"
)

func TestDummyAddPublic(t *testing.T) {
	got := chronological.DummyAdd(8, 4)
	if got != 12 {
		t.Errorf("DummyAdd(8, 4) = %d, want 12", got)
	}
	got = chronological.DummyAdd(-5, 10)
	if got != 5 {
		t.Errorf("DummyAdd(-5, 10) = %d, want 5", got)
	}
	got = chronological.DummyAdd(7, -7)
	if got != 0 {
		t.Errorf("DummyAdd(7, -7) = %d, want 0", got)
	}
}