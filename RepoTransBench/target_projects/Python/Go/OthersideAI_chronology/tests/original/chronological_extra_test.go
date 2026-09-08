package chronological_test

import (
	"testing"

	"github.com/othersideai/chronology/chronological"
)

func TestDummyMul(t *testing.T) {
	got := chronological.DummyMul(2, 3)
	if got != 6 {
		t.Errorf("DummyMul(2, 3) = %d, want 6", got)
	}
	got = chronological.DummyMul(-1, 1)
	if got != -1 {
		t.Errorf("DummyMul(-1, 1) = %d, want -1", got)
	}
	got = chronological.DummyMul(0, 5)
	if got != 0 {
		t.Errorf("DummyMul(0, 5) = %d, want 0", got)
	}
}