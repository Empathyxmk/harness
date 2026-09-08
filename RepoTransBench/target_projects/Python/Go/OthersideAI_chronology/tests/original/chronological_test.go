package chronological_test

import (
	"testing"

	"github.com/othersideai/chronology/chronological"
)

func TestDummyAdd(t *testing.T) {
	got := chronological.DummyAdd(2, 3)
	if got != 5 {
		t.Errorf("DummyAdd(2, 3) = %d, want 5", got)
	}
	got = chronological.DummyAdd(-1, 1)
	if got != 0 {
		t.Errorf("DummyAdd(-1, 1) = %d, want 0", got)
	}
	got = chronological.DummyAdd(0, 0)
	if got != 0 {
		t.Errorf("DummyAdd(0, 0) = %d, want 0", got)
	}
}