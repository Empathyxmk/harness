package public_tests

import (
	"testing"
	"lancegin_haishoku/haishoku/haillow"
)

func TestTupleToHexPublic(t *testing.T) {
	got := haillow.TupleToHex([3]int{12, 210, 111})
	want := "#0cd26f"
	if got != want {
		t.Errorf("TupleToHex((12,210,111)) = %v; want %v", got, want)
	}
}

func TestHexToTuplePublic(t *testing.T) {
	got := haillow.HexToTuple("#123456")
	want := [3]int{18, 52, 86}
	if got != want {
		t.Errorf("HexToTuple('#123456') = %v; want %v", got, want)
	}
}