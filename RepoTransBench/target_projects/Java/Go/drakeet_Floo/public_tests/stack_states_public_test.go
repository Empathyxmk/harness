package public_tests

import "testing"

const (
	ACTIVE    = "ACTIVE"
	PAUSED    = "PAUSED"
	DESTROYED = "DESTROYED"
)

func TestStateValues_public(t *testing.T) {
	if ACTIVE == PAUSED {
		t.Error("ACTIVE and PAUSED should not be equal")
	}
	if PAUSED == DESTROYED {
		t.Error("PAUSED and DESTROYED should not be equal")
	}
}

func TestStateEquality_public(t *testing.T) {
	if ACTIVE != "ACTIVE" {
		t.Error(`ACTIVE should be "ACTIVE"`)
	}
	if ACTIVE == "PAUSED" {
		t.Error(`ACTIVE should not equal "PAUSED"`)
	}
}