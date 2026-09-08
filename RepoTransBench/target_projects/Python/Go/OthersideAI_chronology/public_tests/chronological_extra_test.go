package public_tests

import (
	"testing"

	"github.com/othersideai/chronology/chronological"
)

func TestDummyMulPublic(t *testing.T) {
	got := chronological.DummyMul(4, 5)
	if got != 20 {
		t.Errorf("DummyMul(4, 5) = %d, want 20", got)
	}
	got = chronological.DummyMul(-2, 6)
	if got != -12 {
		t.Errorf("DummyMul(-2, 6) = %d, want -12", got)
	}
	got = chronological.DummyMul(0, -3)
	if got != 0 {
		t.Errorf("DummyMul(0, -3) = %d, want 0", got)
	}
}